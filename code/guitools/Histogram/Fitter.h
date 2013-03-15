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

#ifndef FITTER_H_
#define FITTER_H_

#include <casa/Arrays/Vector.h>
#include <QString>
#include <QTextStream>

namespace casa {

/**
 * Base class for classes performing histogram fits.
 */
class Fitter {
public:
	Fitter();
	void setData( Vector<Float> xValues, Vector<Float> yValues );
	virtual void restrictDomain( double xMin, double xMax );
	virtual void clearDomainLimits();
	Vector<Float> getFitValues() const;
	Vector<Float> getFitValuesX() const;
	virtual bool doFit() = 0;
	virtual void clearFit();

	virtual void toAscii( QTextStream& out ) const;
	bool isFit() const;
	virtual QString getSolutionStatistics() const = 0;
	QString getErrorMessage() const;
	QString getStatusMessage() const;
	virtual ~Fitter();

protected:
	QString formatResultLine( QString label, float value ) const;
	float solutionChiSquared;
	float solutionRMS;
	bool solutionConverged;

	Vector<Float> actualXValues;
	Vector<Float> actualYValues;
	Vector<Float> fitValues;
	QString errorMsg;
	QString statusMsg;
	bool dataFitted;
	float getMean() const;

private:
	void resetDataWithLimits();
	Vector<Float> xValues;
	Vector<Float> yValues;
	double domainMin;
	double domainMax;
};

} /* namespace casa */
#endif /* FITTER_H_ */
