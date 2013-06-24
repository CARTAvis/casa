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

#include "DisplayDataHolder.h"
#include <display/QtViewer/QtDisplayData.qo.h>
#include <display/QtViewer/ImageManager/ImageTracker.h>
#include <algorithm>

namespace casa {

	DisplayDataHolder::DisplayDataHolder()
		: imageTracker( NULL ), imageDisplayer(NULL), controlling_dd(NULL) {
	}


//******************************************************************************
//                  Iteration Support
//******************************************************************************
	int DisplayDataHolder::getCount() const {
		return dataList.size();
	}
	bool DisplayDataHolder::isEmpty() const {
		Bool empty = dataList.empty();
		return empty;
	}

	DisplayDataHolder::DisplayDataIterator DisplayDataHolder::beginDD() const {
		return dataList.begin();
	}

	DisplayDataHolder::DisplayDataIterator DisplayDataHolder::endDD() const {
		return dataList.end();
	}


	bool DisplayDataHolder::exists(QtDisplayData* qdd) const {
		bool exists = false;
		if ( dataList.size() > 0 ) {
			DisplayDataIterator iter = dataList.begin();
			while( iter != dataList.end() ) {
				if(qdd == (*iter)) {
					exists = true;
					break;
				}
				iter++;
			}
		}
		return exists;
	}

	void DisplayDataHolder::setDDControlling( QtDisplayData* controlDD ) {
		//The control dd can be just an open image.  It does not even
		//need to be in the list of registered images.
		if ( controlDD != NULL /*&& exists( controlDD )*/ ) {
			if ( controlling_dd != controlDD ) {
				if ( imageTracker != NULL ) {
					imageTracker->masterImageSelected( controlDD );
				}
				if ( imageDisplayer != NULL ) {
					imageDisplayer->setControllingDD( controlDD );
				}
			}
		}
		controlling_dd = controlDD;
	}

	QtDisplayData* DisplayDataHolder::getChannelDD( int index ) const {
		QtDisplayData* channelDD = NULL;
		if ( dataList.size() > 0 ){
			//By default, the channel dd is the last one in the list
			if ( index < 0 || index >= static_cast<int>(dataList.size())){
				index = dataList.size() - 1;
			}
			DisplayDataIterator iter = dataList.begin();
			int i = 0;
			while (i < index ){
				iter++;
				i++;
			}
			channelDD = (*iter);
		}
		return channelDD;
	}

	QtDisplayData* DisplayDataHolder::getDDControlling( ) const {
		// retrieve the "controlling" DD...
		return controlling_dd;
	}

	QtDisplayData* DisplayDataHolder::getDD(const std::string& name) const {
		// retrieve DD with given name (0 if none).
		QtDisplayData* qdd = NULL;
		DisplayDataIterator iter = dataList.begin();
		while( iter != dataList.end()) {
			if( (*iter)->name() == name ) {
				qdd = (*iter);
				break;
			}
			iter++;
		}
		return qdd;
	}

	void DisplayDataHolder::addDD( QtDisplayData* dd, int position ) {
		//qDebug() << "DisplayDataHolder adding dd size="<<dataList.size();
		if ( ! exists( dd )) {
			if ( position < 0 ) {
				//qDebug()<< "DisplayDataHolder::Putting dd="<<dd->name().c_str()<<" at the end of the list.";
				dataList.push_back( dd);
			} else {
				DisplayDataList::iterator iter = dataList.begin();

				int i = 0;
				while ( i < position ) {
					//qDebug() << "List i="<<i<<" name="<<(*iter)->name().c_str();
					iter++;
					i++;
				}
				//qDebug() << "DisplayDataHolder::at insert i="<<i<<" position="<<position;
				dataList.insert( iter, dd );
			}
			if ( imageTracker != NULL ) {
				imageTracker->imageAdded( dd );
			}
		}
	}

	void DisplayDataHolder::discardDD( QtDisplayData* dd, bool signal ) {
		//First remove the dd from where it current happens to be.
		//If a higher level is available, we do it through calls to
		//the higher layer.  Otherwise, we do it internally.
		if ( exists( dd )) {
			//qDebug() << "DD exists";
			if ( imageDisplayer != NULL ) {
				//qDebug() << "DisplayDataHolder::discardDD Calling unregister";
				imageDisplayer->unregisterDD( dd );
			} else {
				//qDebug() << "DisplayDataHolder::discardDD calling remove";
				removeDD(dd, signal);
			}
		}
	}

	void DisplayDataHolder::insertDD( QtDisplayData* dd, int position ) {
		if ( ! exists(dd) ) {
			//qDebug() << "DisplayData holder insertDD position="<<position;
			//Now put it back in at the proper position.
			if ( imageDisplayer != NULL ) {
				//qDebug() << "Registering dd";
				imageDisplayer->registerDD( dd, position );
			} else {
				//qDebug() << "Skipping registration.";
				addDD( dd, position );
			}
		}
	}


	void DisplayDataHolder::removeDDAll() {
		if ( imageTracker != NULL ) {
			for ( DisplayDataIterator iter = dataList.begin(); iter != dataList.end(); iter++) {
				imageTracker->imageRemoved( *iter );
			}
		}

		dataList.resize(0);
		controlling_dd = NULL;

		//One more notification after the list has been cleared
		//to update the master list.
		if ( imageTracker != NULL ) {
			imageTracker->imageRemoved( NULL );
		}
	}

	bool DisplayDataHolder::removeDD(QtDisplayData* qdd, bool signal ) {
		bool removed = false;
		if ( qdd != NULL && exists( qdd) ) {
			dataList.erase(std::remove(dataList.begin(), dataList.end(), qdd), dataList.end());
			if ( isEmpty() || qdd == controlling_dd ) {
				controlling_dd = NULL;
			}
			if ( imageTracker != NULL && signal ) {
				imageTracker->imageRemoved( qdd );
			}
			removed = true;
		}
		return removed;
	}

	void DisplayDataHolder::setImageTracker( ImageTracker* tracker ) {
		imageTracker = tracker;
	}

	void DisplayDataHolder::setImageDisplayer( ImageDisplayer* displayer ) {
		imageDisplayer = displayer;
	}

	DisplayDataHolder::~DisplayDataHolder() {
		// TODO Auto-generated destructor stub
	}

} /* namespace casa */
