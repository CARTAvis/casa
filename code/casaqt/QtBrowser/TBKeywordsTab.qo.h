//# TBKeywordsTab.qo.h: Widgets used to display table and field keywords.
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
//# $Id: $
#ifndef TBKEYWORDSTAB_H_
#define TBKEYWORDSTAB_H_

#include <casaqt/QtBrowser/TBTableKeywordsTab.ui.h>
#include <casaqt/QtBrowser/TBFieldKeywordsTab.ui.h>
#include <casaqt/QtBrowser/TBNewKeyword.ui.h>

#include <QtGui>

#include <casa/BasicSL/String.h>

namespace casa {

//# Forward Declarations
class TBTable;
class TBTableTabs;
class QCloseableWidget;
class ProgressHelper;
class TBTypes;
class TBArrayPanel;

class TBNewKeyword : public QDialog, Ui::NewKeyword {
    Q_OBJECT

// <summary>
// GUI for entering a new keyword.
// <summary>
//
// <synopsis>
// (Not Completed.)  A TBNewKeyword is a dialog that allows the user to enter a
// new keyword.  The parent/caller is responsible for connecting the signal and
// actually adding the new keyword.
// </synopsis>
    
public:
    // Constructor that takes an optional vector of fields for entering a new
	// field keyword.  If this vector is null, a table keyword is entered.
    TBNewKeyword(std::vector<casacore::String>* fields = NULL, QWidget* parent = NULL);

    ~TBNewKeyword();

signals:
    // newKeyword is emitted when the user has entered a new keyword.  The
	// field index is -1 for a table keyword; otherwise it holds the index of
	// the field to which the keyword should be added.
    void newKeyword(int field, casacore::String name, casacore::String type, void* value);

private:
    // Displayed data types.
    std::vector<casacore::String>* types;

    // Widget to enter the value based on the type.
    TBTypes* typesWidget;

private slots:
    // Catches when the user changes the type and changes the types widget
	// accordingly.
    void typeChanged(int index);
};

// <summary>
// Widget used to display table keywords.
// <summary>
//
// <synopsis>
// casacore::Table keywords are displayed in a QTableWidget which cannot be edited.
// double-clicking certain types of keywords has certain effects:
// double-clicking a table keyword will open that subtable while
// double-clicking an array will open the array in a side panel.
// </synopsis>

class TBTableKeywordsTab : public QWidget, Ui::TableKeywordsTab {
    Q_OBJECT

public:
    // Constructor which takes pointers to the table backend.
    TBTableKeywordsTab(TBTableTabs* tt, TBTable* t);

    ~TBTableKeywordsTab();

    
    // Returns the table widget used to display the keywords.
    QTableWidget* getTableWidget();

    
    // Updates the QTableWidget with the new data that has been loaded into the
    // table backend.  If a ProgressHelper is provided, it will be updated
    // periodically with progress information.
    void updateTable(ProgressHelper* pp = NULL);

public slots:
    // Clears whatever widget (if any) is currently being displayed in the side
	// panel.
    void clearWidgetInSplitter();

    // Show the given widget on the right side of the splitter.
    void showWidgetInSplitter(QWidget* widget);
    
signals:
    // This signal is emitted when the right widget is closed.  The QWidget
	// points to the widget that was just closed.
    void rightWidgetClosed(QWidget* widget);

private:
    // Useful pointers to table backend.
    TBTableTabs* ttabs;
    TBTable* table;

    // Flag on whether events generated by the QTableWidget are "genuine."
    bool update;

    // Side panel.
    QCloseableWidget* rightWidget;
    
    // casacore::Array panel.
    TBArrayPanel* arrayPanel;

private slots:
    // Slot for when a keyword is double-clicked.
    void doubleClicked(int row, int col);

    // Slot for "Add Keyword" button.  (Not currently implemented.)
    void addKeyword();

    // Slot for "Edit Keyword" button.  (Not currently implemented.)
    void editKeyword();

    // Slot for "Remove Keyword" button.  (Not currently implemented.)
    void removeKeyword();

    // Slot for when a keyword is selected in the table.
    void cellSelected(int row);
};

// <summary>
// Widget used to display field keywords.
// <summary>
//
// <synopsis>
// Field keywords are displayed in a QTreeWidget which cannot be edited.
// double-clicking certain types of keywords has certain effects:
// double-clicking a table keyword will open that subtable while
// double-clicking an array will open the array in a side panel.
// </synopsis>

class TBFieldKeywordsTab : public QWidget, Ui::FieldKeywordsTab {
    Q_OBJECT

public:
    // Constructor which takes pointers to the table backend.
    TBFieldKeywordsTab(TBTableTabs* tt, TBTable* t);

    ~TBFieldKeywordsTab();

    
    // Returns the QTreeWidget in which the field keywords are displayed.
    QTreeWidget* getTreeWidget();

    
    // Updates the QTreeWidget with the new data that has been loaded into the
    // table backend.  If a ProgressHelper is provided, it will be updated
    // periodically with progress information.
    void updateTable(ProgressHelper* pp = NULL);

public slots:
    // Clears whatever widget (if any) is currently being displayed in the side
	// panel.
    void clearWidgetInSplitter();

    // Show the given widget on the right side of the splitter.
    void showWidgetInSplitter(QWidget* widget);
    
signals:
    // This signal is emitted when the right widget is closed.  The QWidget
	// points to the widget that was just closed.
    void rightWidgetClosed(QWidget* widget);

private:
    // Useful pointers to the table backend.
    TBTableTabs* ttabs;
    TBTable* table;

    // Flag on whether events generated by the QTableWidget are "genuine."
    bool update;

    // Side panel.
    QCloseableWidget* rightWidget;
    
    // casacore::Array panel.
    TBArrayPanel* arrayPanel;
    
private slots:
    // Slot for when a field keyword is double-clicked.
    void doubleClicked(QTreeWidgetItem* item, int col);
};

}

#endif /* TBKEYWORDSTAB_H_ */
