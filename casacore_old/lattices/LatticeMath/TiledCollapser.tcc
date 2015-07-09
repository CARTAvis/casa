//# TiledCollapser.cc: Abstract base class to collapse lines
//# Copyright (C) 1996,1997
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
//# $Id: TiledCollapser.tcc 21563 2015-02-16 07:05:15Z gervandiepen $

#ifndef LATTICES_TILEDCOLLAPSER_TCC
#define LATTICES_TILEDCOLLAPSER_TCC


#include <casacore/lattices/LatticeMath/TiledCollapser.h>


namespace casacore { //# NAMESPACE CASACORE - BEGIN

template<class T, class U>
TiledCollapser<T,U>::~TiledCollapser()
{}

template<class T, class U>
Bool TiledCollapser<T,U>::canHandleNullMask() const
{
    return False;
}

} //# NAMESPACE CASACORE - END


#endif