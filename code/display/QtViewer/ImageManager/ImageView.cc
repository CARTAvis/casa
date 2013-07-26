//# Copyright (C) 2005
//# Associated Universities, Inc. Washington DC, USA.
//#
//# This library is free software; you can redistribute it and/or modify it
//# under the terms of the GNU Library General Public License as published by
//# the Free Software Foundation; either version 2 of the License, or (at your
//# option) any later version.
//#
//# This library is distributed in the hope that it will be useful, but WITHOUT
//# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
//# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Library General Public
//# License for more details.
//#
//# You should have received a copy of the GNU Library General Public License
//# along with this library; if not, write to the Free Software Foundation,
//# Inc., 675 Massachusetts Ave, Cambridge, MA 02139, USA.
//#
//# Correspondence concerning AIPS++ should be addressed as follows:
//#        Internet email: aips2-request@nrao.edu.
//#        Postal address: AIPS++ Project Office
//#                        National Radio Astronomy Observatory
//#                        520 Edgemont Road
//#                        Charlottesville, VA 22903-2475 USA
//#
#include "ImageView.qo.h"
#include <casa/BasicSL/String.h>
#include <display/QtViewer/ImageManager/ImageView.qo.h>
#include <display/QtViewer/ImageManager/DisplayLabel.qo.h>
#include <display/QtViewer/QtDisplayData.qo.h>

#include <QUuid>
#include <QDrag>
#include <QMenu>
#include <QColorDialog>
#include <QMouseEvent>
#include <QPainter>


namespace casa {
	const QString ImageView::DROP_ID = "Image Name";
	ImageView::ImageView(QtDisplayData* data, QWidget *parent)
		: QFrame(parent),
		  closeAction( "Close", this ),
		  masterCoordinateSystemAction( "Coordinate System Master", this ),
		  masterCoordinateSystemUndoAction( "Clear Coordinate System Master", this ),
		  masterHueAction( "Hue Master", this ),
		  masterSaturationAction( "Saturation Master", this ),
		  normalColor("#D3D3D3"),
		  masterCoordinateColor("#BABABA" ),
		  imageData( NULL ),
		  REST_FREQUENCY_KEY("axislabelrestvalue"),
		  VALUE_KEY( "value"),
		  SIZE_COLLAPSED( 50 ), SIZE_EXPANDED( 200 ){

		ui.setupUi(this);
		initDisplayLabels();
		minimumSize = SIZE_COLLAPSED;
		setSizePolicy( QSizePolicy::MinimumExpanding, QSizePolicy::Fixed );

		//Context Menu
		setContextMenuPolicy( Qt::CustomContextMenu );
		connect( this, SIGNAL( customContextMenuRequested( const QPoint&)), this, SLOT(showContextMenu( const QPoint&)) );

		if ( data != NULL ) {
			imageData = data;
		}

		//Rest frequency/wavelength information
		initRestSettings();

		//Registration
		ui.selectCheckBox->setChecked( false );
		connect( ui.selectCheckBox, SIGNAL(toggled(bool)),
				this, SLOT(imageRegistrationChanged(bool)));

		//Color settings
		setBackgroundColor( normalColor );
		setAutoFillBackground( true );
		initColorModeSettings();

		//Data options
		connect( ui.dataOptionsButton, SIGNAL(clicked()), this, SLOT(showDataOptions()));

		//Title of the image
		setTitle();

		//Display type of the image
		initDisplayType();

		//Open close the image view.
		minimizeDisplay();
		connect( ui.openCloseButton, SIGNAL(clicked()), this, SLOT(openCloseDisplay()));
	}

	void ImageView::setTitle(){
		QString name;
		if ( imageData == NULL ) {
			QUuid uid = QUuid::createUuid();
			name = uid.toString();
		}
		else {
			String imageName = imageData->name();
			name = imageName.c_str();
		}
		ui.imageNameLabel->setText( name );
	}

	void ImageView::initColorModeSettings(){
		ui.colorLabel->setAutoFillBackground( true );
		colorMode = NO_COMBINATION;
		setColorCombinationMode( colorMode );
		setButtonColor( normalColor );
		QButtonGroup* colorGroup = new QButtonGroup( this );
		colorGroup->addButton( ui.redRadio );
		colorGroup->addButton( ui.greenRadio );
		colorGroup->addButton( ui.blueRadio );
		colorGroup->addButton( ui.otherRadio );
		ui.otherRadio->setChecked( true );
		connect( ui.redRadio, SIGNAL(clicked()), this, SLOT(rgbChanged()));
		connect( ui.greenRadio, SIGNAL(clicked()), this, SLOT(rgbChanged()));
		connect( ui.blueRadio, SIGNAL(clicked()), this, SLOT(rgbChanged()));
		connect( ui.otherRadio, SIGNAL(clicked()), this, SLOT(otherColorChanged()));
		connect( ui.colorButton, SIGNAL(clicked()), this, SLOT(showColorDialog()));
		otherColorChanged();
	}

	void ImageView::initDisplayLabel( QWidget* holder, DisplayLabel* label ){
		QVBoxLayout* verticalLayout = new QVBoxLayout();
		verticalLayout->setContentsMargins( 0, 0, 0, 3 );
		verticalLayout->addWidget( label, Qt::AlignTop | Qt::AlignCenter );
		//verticalLayout->addStretch( 1 );
		holder->setLayout( verticalLayout );
	}

	void ImageView::initDisplayLabels(){
		displayTypeLabel = new DisplayLabel( 1, this );
		initDisplayLabel( ui.displayTypeHolder, displayTypeLabel );

		coordinateMasterLabel = new DisplayLabel( 1, this );
		initDisplayLabel( ui.coordinateMasterHolder, coordinateMasterLabel );

		hueMasterLabel = new DisplayLabel( 1, this );
		initDisplayLabel( ui.hueMasterHolder, hueMasterLabel );

		saturationMasterLabel = new DisplayLabel( 1, this );
		initDisplayLabel( ui.saturationMasterHolder, saturationMasterLabel );
	}

	void ImageView::initDisplayType() {
		displayGroup = new QButtonGroup( this );
		displayGroup->addButton( ui.contourRadio, DISPLAY_CONTOUR );
		displayGroup->addButton( ui.rasterRadio, DISPLAY_RASTER );
		displayGroup->addButton( ui.vectorRadio, DISPLAY_VECTOR );
		displayGroup->addButton( ui.markerRadio, DISPLAY_MARKER );
		displayTypeMap.insert( DISPLAY_CONTOUR, "C");
		displayTypeMap.insert( DISPLAY_RASTER, "R");
		displayTypeMap.insert( DISPLAY_VECTOR, "V");
		displayTypeMap.insert( DISPLAY_MARKER, "M");
		if ( imageData != NULL ) {
			if ( imageData->isContour() ) {
				ui.contourRadio->setChecked(true);
				displayTypeLabel->setText( displayTypeMap[DISPLAY_CONTOUR] );
				storedDisplay = DISPLAY_CONTOUR;
			} else if ( imageData->isRaster() ) {
				ui.rasterRadio->setChecked( true );
				storedDisplay = DISPLAY_RASTER;
				displayTypeLabel->setText( displayTypeMap[DISPLAY_RASTER] );
			} else if ( imageData->isMarker()) {
				ui.markerRadio->setChecked( true );
				storedDisplay = DISPLAY_MARKER;
				displayTypeLabel->setText( displayTypeMap[DISPLAY_MARKER] );
			} else if ( imageData->isVector()) {
				ui.vectorRadio->setChecked( true );
				storedDisplay = DISPLAY_VECTOR;
				displayTypeLabel->setText( displayTypeMap[DISPLAY_VECTOR] );
			}
		}
		connect( ui.contourRadio, SIGNAL(clicked()), this, SLOT(displayTypeChanged()));
		connect( ui.rasterRadio, SIGNAL(clicked()), this, SLOT(displayTypeChanged()));
		connect( ui.vectorRadio, SIGNAL(clicked()), this, SLOT(displayTypeChanged()));
		connect( ui.markerRadio, SIGNAL(clicked()), this, SLOT(displayTypeChanged()));
	}


	//-----------------------------------------------------------------------------
	//              Getters
	//-----------------------------------------------------------------------------

	bool ImageView::isControlEligible() const {
		bool controlEligible = false;
		if ( imageData != NULL ) {
			if ( imageData->isImage() ) {
				if ( imageData->dd()->isDisplayable() && imageData->imageInterface() != NULL ) {
					controlEligible = true;
				}
			}
		}
		return controlEligible;
	}

	bool ImageView::isRegistered() const {
		return ui.selectCheckBox->isChecked();
	}

	QtDisplayData* ImageView::getData() const {
		return imageData;
	}

	QString ImageView::getDataDisplayTypeName() const {
		QAbstractButton* button = displayGroup->checkedButton();
		return button->text();
	}

	bool ImageView::isMasterHue() const {
		bool masterHue = false;
		if ( hueMasterLabel != NULL ){
			masterHue = !hueMasterLabel->isEmpty();
		}
		return masterHue;
	}

	bool ImageView::isMasterSaturation() const {
		bool masterSaturation = false;
		if ( saturationMasterLabel != NULL ){
			masterSaturation = !saturationMasterLabel->isEmpty();
		}
		return masterSaturation;
	}

	bool ImageView::isMasterCoordinate() const {
		bool masterCoordinate = !coordinateMasterLabel->isEmpty();
		return masterCoordinate;
	}

	QString ImageView::getName() const {
		QString nameStr = ui.imageNameLabel->text();
		return nameStr;
	}


	//---------------------------------------------------------------------------------
	//                     Rest Frequency/Wavelength
	//---------------------------------------------------------------------------------

	void ImageView::initRestSettings(){
		frequencyUnits = (QStringList() << "Hz"<<"MHz"<<"GHz");
		wavelengthUnits = (QStringList() << "mm"<<"um"<<"nm"<<"Angstrom");
		double maxValue = std::numeric_limits<double>::max();
		double minValue = 0;
		QValidator* restValidator = new QDoubleValidator( minValue, maxValue, 8, this);
		ui.restLineEdit->setValidator( restValidator );
		for ( int i = 0; i < frequencyUnits.size(); i++ ){
			ui.restUnitsCombo->addItem( frequencyUnits[i]);
		}
		for ( int i = 0; i < wavelengthUnits.size(); i++ ){
			ui.restUnitsCombo->addItem( wavelengthUnits[i]);
		}
		Record options = imageData->getOptions();
		if ( options.isDefined( REST_FREQUENCY_KEY)){
			Record restRecord = options.asRecord( REST_FREQUENCY_KEY);
			String restValueStr = restRecord.asString( VALUE_KEY);
			QString restUnits;
			String restValue;
			int unitsIndex = -1;
			for ( int i = 0; i < frequencyUnits.size(); i++ ){
				unitsIndex = restValueStr.index( frequencyUnits[i].toStdString());
				if ( unitsIndex >= 0 ){
					restValue = restValueStr.before(unitsIndex );
					restUnits = frequencyUnits[i];
					break;
				}
			}
			if ( unitsIndex < 0 ){
				for ( int i = 0; i < wavelengthUnits.size(); i++ ){
					unitsIndex = restValueStr.index( wavelengthUnits[i].toStdString());
					if ( unitsIndex >= 0 ){
						restValue = restValueStr.before( unitsIndex );
						restUnits = wavelengthUnits[i];
						break;
					}
				}
			}
			if ( unitsIndex >= 0 ){
				ui.restLineEdit->setText( restValue.c_str());
				int index = ui.restUnitsCombo->findText( restUnits );
				ui.restUnitsCombo->setCurrentIndex( index );
			}
			else {
				qDebug() << "Could not parse: "<<restValueStr.c_str();
			}
		}
		//cout << options << endl;
		connect( ui.restLineEdit, SIGNAL(editingFinished()), this, SLOT(restFrequencyChanged()));
		connect( ui.restUnitsCombo, SIGNAL(currentIndexChanged(int)), this, SLOT(restFrequencyChanged()));
	}

	void ImageView::restFrequencyChanged(){
		QString valueStr = ui.restLineEdit->text();
		QString unitStr = ui.restUnitsCombo->currentText();
		if ( valueStr.length() > 0 ){
			String comboStr(valueStr.toStdString());
			comboStr.append( unitStr.toStdString());
			Record dataOptions = imageData->getOptions();
			Record restRecord = dataOptions.asRecord( REST_FREQUENCY_KEY );
			restRecord.define( VALUE_KEY, comboStr );
			dataOptions.defineRecord( REST_FREQUENCY_KEY, restRecord );
			imageData->setOptions( dataOptions );
		}
	}


	//--------------------------------------------------------------------
	//                    Setters
	//--------------------------------------------------------------------

	void ImageView::setMasterCoordinateImage( bool masterImage ){
		if ( masterImage ){
			setBackgroundColor( masterCoordinateColor );
			coordinateMasterLabel->setText( "C");
		}
		else {
			setBackgroundColor( normalColor );
			coordinateMasterLabel->setText( "");
		}
	}

	void ImageView::setMasterHueImage( bool masterImage ){
		if ( masterImage ){
			hueMasterLabel->setText( "H");
		}
		else {
			hueMasterLabel->setText( "");
		}
	}
	void ImageView::setMasterSaturationImage( bool masterImage ){
		if ( masterImage ){
			saturationMasterLabel->setText( "S");
		}
		else {
			saturationMasterLabel->setText( "");
		}
	}

	void ImageView::setRegistered( bool selected ) {
		ui.selectCheckBox->setChecked( selected );
	}

	void ImageView::setColorCombinationMode( ColorCombinationMode mode ){
		colorMode = mode;
	}

	void ImageView::setViewedImage( bool viewed ){
		if ( viewed ){
			setFrameStyle( QFrame::Box | QFrame::Sunken );
			setLineWidth( 5 );
		}
		else {
			setFrameStyle( QFrame::Plain );
			setLineWidth( 2 );
		}
	}


	//-----------------------------------------------------------------------
	//             Context Menu
	//-----------------------------------------------------------------------

	void ImageView::showContextMenu( const QPoint& location ) {

		//Set-up the context
		QPoint showLocation = mapToGlobal( location );
		QMenu contextMenu;
		bool masterCoordinateImage = isMasterCoordinate();
		if ( !masterCoordinateImage && isControlEligible() ){
			contextMenu.addAction( &masterCoordinateSystemAction );
		}
		else if (masterCoordinateImage ){
			contextMenu.addAction( &masterCoordinateSystemUndoAction );
		}
		if ( !isMasterHue() ){
			contextMenu.addAction( &masterHueAction );
		}
		if ( !isMasterSaturation() ){
			contextMenu.addAction( &masterSaturationAction );
		}
		contextMenu.addAction( &closeAction );

		//Act on the user's selection.
		QAction* selectedAction = contextMenu.exec( showLocation );
		if ( selectedAction == &closeAction ){
			emit close( this );
		}
		else if ( selectedAction == &masterCoordinateSystemAction ){
			setMasterCoordinateImage( true );
			emit masterCoordinateImageSelected( this );
		}
		else if ( selectedAction == &masterCoordinateSystemUndoAction ){
			setMasterCoordinateImage( false );
			emit masterCoordinateImageClear();
		}
		else if ( selectedAction == &masterHueAction ){
			setMasterHueImage( true );
			emit masterHueImageSelected( this );
		}
		else if ( selectedAction == &masterSaturationAction ){
			setMasterSaturationImage( true );
			emit masterSaturationImageSelected( this );
		}
	}


	//-----------------------------------------------------------
	//            Color
	//-----------------------------------------------------------

	void ImageView::setBackgroundColor( QColor color ) {
		QPalette pal = palette();
		pal.setColor( QPalette::Background, color );
		setPalette( pal );
		displayTypeLabel->setEmptyColor( color );
		coordinateMasterLabel->setEmptyColor( color );
		hueMasterLabel->setEmptyColor( color );
		saturationMasterLabel->setEmptyColor( color );
	}

	QColor ImageView::getBackgroundColor() const {
		QPalette pal = palette();
		return pal.color( QPalette::Background );
	}

	QColor ImageView::getButtonColor() const {
		QPalette p = ui.colorButton->palette();
		QBrush brush = p.brush(QPalette::Button );
		QColor backgroundColor = brush.color();
		return backgroundColor;
	}

	void ImageView::setButtonColor( QColor color ){
		QPalette p = ui.colorButton->palette();
		p.setBrush(QPalette::Button, color);
		ui.colorButton->setPalette( p );
	}

	void ImageView::showColorDialog(){
		QColor initialColor = getButtonColor();
		QColor selectedColor = QColorDialog::getColor( initialColor, this );
		if ( selectedColor.isValid() ){
			setButtonColor( selectedColor );
			rgbChanged();
		}
	}

	QColor ImageView::getDisplayedColor() const {
		QColor displayedColor = Qt::black;
		const int MAX_COLOR = 255;
		if ( ui.otherRadio->isChecked()){
			displayedColor = getButtonColor();
		}
		else if ( ui.redRadio->isChecked()){
			displayedColor.setRed( MAX_COLOR );
		}
		else if ( ui.greenRadio->isChecked()){
			displayedColor.setGreen( MAX_COLOR );
		}
		else if ( ui.blueRadio -> isChecked()){
			displayedColor.setBlue( MAX_COLOR );
		}
		displayedColor.setAlpha(127);
		return displayedColor;
	}

	void ImageView::setDisplayedColor( QColor rgbColor ){
		int redAmount = rgbColor.red();
		int greenAmount = rgbColor.green();
		int blueAmount = rgbColor.blue();
		const int MAX_COLOR = 255;
		if ( redAmount == MAX_COLOR && blueAmount == 0 && greenAmount == 0 ){
			ui.redRadio->setChecked( true );
		}
		else if (redAmount == 0 && blueAmount == MAX_COLOR && greenAmount == 0){
			ui.blueRadio->setChecked( true );
		}
		else if ( redAmount == 0 && blueAmount == 0 && greenAmount == MAX_COLOR){
			ui.greenRadio->setChecked( true );
		}
		else {
			setButtonColor( rgbColor );
			ui.otherRadio->setChecked( true );
		}
		rgbChanged();
	}

	void ImageView::rgbChanged(){
		QColor baseColor = getDisplayedColor();
		QPalette pal = ui.colorLabel->palette();
		pal.setColor( QPalette::Background, baseColor );
		ui.colorLabel->setPalette( pal );
	}

	void ImageView::otherColorChanged(){
		ui.colorButton->setEnabled( ui.otherRadio->isChecked());
		rgbChanged();
	}

	//----------------------------------------------------------------
	//            Slots
	//----------------------------------------------------------------

	void ImageView::displayTypeChanged() {
		//Decide if there has been a change to Raster/Color/Contour/Vector
		DisplayType guiDisplay = static_cast<DisplayType>(displayGroup->checkedId());
		if ( storedDisplay != guiDisplay ){
			storedDisplay = guiDisplay;

			//Update the quick-look label
			displayTypeLabel->setText( displayTypeMap[guiDisplay] );

			//Change the underlying data type
			emit displayTypeChanged( this );
		}
	}

	void ImageView::imageRegistrationChanged( bool /*selected*/ ) {
		emit imageSelected( this );
	}


	void ImageView::showDataOptions(){
		emit showDataDisplayOptions( imageData );
	}


	//-----------------------------------------------------------------------------
	//                 Opening/Closing
	//-----------------------------------------------------------------------------

	QSize ImageView::minimumSizeHint() const {
		QSize frameSize = QFrame::size();
		QSize hint ( /*frameSize.width()*/700, minimumSize );
		return hint;
	}

	void ImageView::openCloseDisplay() {
		if ( minimumSize == SIZE_COLLAPSED ) {
			maximizeDisplay();
		} else {
			minimizeDisplay();
		}

		updateGeometry();
	}

	void ImageView::minimizeDisplay() {
		ui.widgetLayout->removeWidget( ui.displayGroupBox );
		ui.widgetLayout->removeWidget( ui.colorGroupBox);
		ui.widgetLayout->removeWidget( ui.restGroupBox );
		ui.displayOptionsLayout->removeWidget( ui.dataOptionsButton );

		ui.displayGroupBox->setParent( NULL );
		ui.colorGroupBox->setParent( NULL );
		ui.restGroupBox->setParent( NULL );
		ui.dataOptionsButton->setParent( NULL );

		minimumSize = SIZE_COLLAPSED;
		QIcon openIcon( ":/icons/imageMaximize.png");
		ui.openCloseButton->setIcon( openIcon );
	}

	void ImageView::maximizeDisplay() {
		ui.widgetLayout->addWidget( ui.displayGroupBox );
		ui.widgetLayout->addWidget( ui.restGroupBox );
		ui.widgetLayout->addWidget( ui.colorGroupBox );
		ui.displayOptionsLayout->insertWidget( 1, ui.dataOptionsButton );
		minimumSize = SIZE_EXPANDED;
		QIcon closeIcon( ":/icons/imageMinimize.png");
		ui.openCloseButton->setIcon( closeIcon );
	}


	//**********************************************************************
	//                   Drag and Drop
	//**********************************************************************

	QImage* ImageView::makeDragImage(){
		QSize viewSize = size();
		QImage* dragImage = new QImage( viewSize.width(), viewSize.height(), QImage::Format_ARGB32_Premultiplied );
		const int GRAY_SHADE = 200;
		dragImage->fill(qRgba(GRAY_SHADE,GRAY_SHADE,GRAY_SHADE,255));
		QPainter painter;
		painter.begin(dragImage);
		const int PEN_WIDTH = 2;
		QPen pen;
		pen.setStyle(Qt::DashLine );
		pen.setWidth( PEN_WIDTH );
		pen.setColor( Qt::black );
		painter.setPen( pen );
		int width = dragImage->width() - PEN_WIDTH;
		int height = dragImage->height() - PEN_WIDTH;
		painter.drawRect( QRect(1,1, width, height));
		QFontMetrics metrics = painter.fontMetrics();
		QString title = getName();
		int x = ( width - metrics.width( title )) / 2;
		int y = height / 2 + 5;
		painter.drawText(x, y, title );
		painter.end();
		return dragImage;
	}

	void ImageView::makeDrag( QMouseEvent* event ) {
		QDrag* drag = new QDrag( this );
		QMimeData* mimeData = new QMimeData();
		QByteArray itemId = getName().toAscii();
		mimeData->setData( DROP_ID, itemId );
		QImage* dragImage = makeDragImage();
		drag->setPixmap( QPixmap::fromImage(*dragImage));
		drag->setMimeData( mimeData );
		QPoint hotSpot = event->pos();
		QByteArray itemData;
		QDataStream dataStream( &itemData, QIODevice::WriteOnly );
		dataStream << hotSpot;
		mimeData->setData( "application/manage_images", itemData );
		drag->setHotSpot( hotSpot );
		drag->start();
	}

	void ImageView::mouseMoveEvent( QMouseEvent* event ) {
		makeDrag( event );
	}

	ImageView::~ImageView() {
	}
}
