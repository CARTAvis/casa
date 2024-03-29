#
# CASA - Common Astronomy Software Applications
# Copyright (C) 2010 by ESO (in the framework of the ALMA collaboration)
#
# This file is part of CASA.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


BISON_TARGET (CalLibraryGram CalLibrary/CalLibraryGram.yy ${CMAKE_CURRENT_BINARY_DIR}/CalLibraryGram.ycc COMPILE_FLAGS "-y -p CalLibraryGram --output-file=CalLibraryGram.ycc")
FLEX_TARGET (CalLibraryGram CalLibrary/CalLibraryGram.ll ${CMAKE_CURRENT_BINARY_DIR}/CalLibraryGram.lcc COMPILE_FLAGS "-PCalLibraryGram")

include_directories (${CMAKE_CURRENT_BINARY_DIR})

casa_add_library( synthesis
 TransformMachines2/Utils.cc
  TransformMachines2/BeamSkyJones.cc
  TransformMachines2/ComponentFTMachine.cc
 TransformMachines2/VLAIlluminationConvFunc.cc
  TransformMachines2/GridFT.cc	
  TransformMachines2/HetArrayConvFunc.cc
  TransformMachines2/FTMachine.cc
  TransformMachines2/MosaicFT.cc
  TransformMachines2/MosaicFTNew.cc
  TransformMachines2/MultiTermFTNew.cc
  TransformMachines2/SetJyGridFT.cc
  TransformMachines2/SimplePBConvFunc.cc	
  TransformMachines2/SimpleComponentFTMachine.cc
  TransformMachines2/SkyJones.cc
  TransformMachines2/VisModelData.cc
  TransformMachines2/VPSkyJones.cc
  TransformMachines2/WPConvFunc.cc
  TransformMachines2/WProjectFT.cc
#  TransformMachines2/CFCell.cc
  TransformMachines2/ConvolutionFunction.cc
 TransformMachines2/AWProjectFT.cc
 TransformMachines2/AWProjectWBFT.cc
 TransformMachines2/AWProjectWBFTNew.cc
 TransformMachines2/CFBuffer.cc
 TransformMachines2/EVLAAperture.cc
 TransformMachines2/AzElAperture.cc
 TransformMachines2/CFStore.cc
 TransformMachines2/CFStore2.cc
 TransformMachines2/ATerm.cc
 TransformMachines2/PSTerm.cc
 TransformMachines2/WTerm.cc
 TransformMachines2/VLACalcIlluminationConvFunc.cc
 TransformMachines2/IlluminationConvFunc.cc
 TransformMachines2/CFCache.cc
 TransformMachines2/AWConvFuncEPJones.cc
 TransformMachines2/AWConvFunc.cc
  TransformMachines2/PolOuterProduct.cc
  TransformMachines2/AWVisResampler.cc
 TransformMachines2/VisibilityResamplerBase.cc
 TransformMachines2/VisibilityResampler.cc
  TransformMachines/BeamSkyJones.cc
  TransformMachines/BeamSquint.cc
  TransformMachines/CFCache.cc
  TransformMachines/CFStore.cc
  TransformMachines/CFStore2.cc
  TransformMachines/CFBuffer.cc
  TransformMachines/CFCell.cc
  TransformMachines/PolOuterProduct.cc
  TransformMachines/ComponentFTMachine.cc
  TransformMachines/ConvolutionFunction.cc
  TransformMachines/AWConvFunc.cc
#  TransformMachines/AWConvFunc2.cc
  TransformMachines/AWConvFuncEPJones.cc
  TransformMachines/AWProjectFT.cc
  TransformMachines/AWProjectWBFT.cc
  TransformMachines/AWProjectWBFTNew.cc
  TransformMachines/AWVisResampler.cc
#  TransformMachines/ProtoVR.cc
#  TransformMachines/cDataToGridImpl.cc
  TransformMachines/BeamCalc.cc
  TransformMachines/BeamCalcParams.cc
  TransformMachines/DBeamSkyJones.cc
  TransformMachines/FTMachine.cc
  TransformMachines/GridFT.cc
  TransformMachines/SetJyGridFT.cc
  TransformMachines/rGridFT.cc
  TransformMachines/HetArrayConvFunc.cc
  TransformMachines/MosaicFT.cc
  TransformMachines/MosaicFTNew.cc
  TransformMachines/MultiTermFT.cc	
  TransformMachines/MultiTermFTNew.cc	
  TransformMachines/NewMultiTermFT.cc	
  TransformMachines/PBMath1DAiry.cc
  TransformMachines/PBMath1D.cc
  TransformMachines/PBMath1DCosPoly.cc
  TransformMachines/PBMath1DEVLA.cc
  TransformMachines/PBMath1DGauss.cc
  TransformMachines/PBMath1DIPoly.cc
  TransformMachines/PBMath1DNumeric.cc
  TransformMachines/PBMath1DPoly.cc
  TransformMachines/PBMath2D.cc
  TransformMachines/PBMath2DImage.cc
  TransformMachines/PBMath.cc
  TransformMachines/PBMathInterface.cc
  TransformMachines/SimpCompGridMachine.cc
  TransformMachines/SimpComponentGridMachine.cc
  TransformMachines/SimpleComponentFTMachine.cc
  TransformMachines/SimplePBConvFunc.cc
  TransformMachines/SkyJones.cc
  TransformMachines/StokesImageUtil.cc
  TransformMachines/SynthesisError.cc
  TransformMachines/Utils.cc
  TransformMachines/VisModelData.cc
  TransformMachines/VPSkyJones.cc
  TransformMachines/WProjectFT.cc
  TransformMachines/WPConvFunc.cc
  TransformMachines/EVLAConvFunc.cc
  TransformMachines/ATerm.cc
  TransformMachines/EVLAAperture.cc
  TransformMachines/AzElAperture.cc
  fortran/fgridft.f		
  fortran/fmosaic.f
  fortran/wprojgrid.f
  fortran/faccumulateToGrid.f
  fortran/faccumulateFromGrid.f
  fortran/fgridsdclip.f
  CalLibrary/CalLibraryTools.cc
  CalLibrary/CalLibraryParse.cc
  CalTables/BJonesDesc.cc
  CalTables/BJonesMBuf.cc
  CalTables/BJonesMCol.cc
  CalTables/BJonesMRec.cc
  CalTables/BJonesTable.cc
  CalTables/CalBuffer.cc
  CalTables/CalDescBuffer.cc
  CalTables/CalDescColumns2.cc
  CalTables/CalDescColumns.cc
  CalTables/CalDescRecord.cc
  CalTables/CalHistoryBuffer.cc
  CalTables/CalHistoryColumns.cc
  CalTables/CalHistRecord.cc
  CalTables/CalInterp.cc
  CalTables/CalInterpolation.cc
  CalTables/CalInterpolator.cc
  CalTables/CalIntpMatch.cc
  CalTables/CalIter.cc
  CalTables/CalMainBuffer.cc
  CalTables/CalMainColumns.cc
  CalTables/CalMainRecord.cc
  CalTables/CalSet2.cc
  CalTables/CalSetMetaInfo.cc
  CalTables/CalTable2.cc
  CalTables/CalTable.cc
  CalTables/CalTableDesc2.cc
  CalTables/CalTableDesc.cc
  CalTables/CLPatchPanel.cc
  CalTables/CTColumns.cc
  CalTables/CTDesc.cc
  CalTables/CTEnums.cc
  CalTables/CTGlobals.cc
  CalTables/CTInterface.cc
#  CalTables/CTSelection.cc
  CalTables/CTIter.cc
  CalTables/CTMainColumns.cc
  CalTables/CTMainRecord.cc
  CalTables/CTPatchedInterp.cc
  CalTables/CTTimeInterp1.cc
  CalTables/EPointDesc.cc
  CalTables/EPointMBuf.cc
  CalTables/EPointMCol.cc
  CalTables/EPointTable.cc
  CalTables/EPointVJMRec.cc
  CalTables/FVisJonesDesc.cc
  CalTables/FVisJonesMRec.cc
  CalTables/GJonesDesc.cc
  CalTables/GJonesMBuf.cc
  CalTables/GJonesMCol.cc
  CalTables/GJonesTable.cc
  CalTables/MJonesDesc.cc
  CalTables/MJonesMRec.cc
  CalTables/NewCalTable.cc
  CalTables/RIorAParray.cc
  CalTables/SolvableMJDesc.cc
  CalTables/SolvableMJMRec.cc
  CalTables/SolvableVJDesc.cc
  CalTables/SolvableVJMBuf.cc
  CalTables/SolvableVJMCol.cc
  CalTables/SolvableVJMRec.cc
  CalTables/SolvableVJTable.cc
  CalTables/TimeVarMJDesc.cc
  CalTables/TimeVarMJMRec.cc
  CalTables/TimeVarVJDesc.cc
  CalTables/TimeVarVJMBuf.cc
  CalTables/TimeVarVJMCol.cc
  CalTables/TimeVarVJMRec.cc
  CalTables/TimeVarVJTable.cc
  CalTables/TJonesDesc.cc
  CalTables/TJonesMBuf.cc
  CalTables/TJonesMCol.cc
  CalTables/TJonesTable.cc
  CalTables/VisJonesDesc.cc
  CalTables/VisJonesMBuf.cc
  CalTables/VisJonesMCol.cc
  CalTables/VisJonesMRec.cc
  CalTables/VisJonesTable.cc
  Parallel/Applicator.cc
 Parallel/MPIError.cc
 Parallel/MPITransport.cc
 Parallel/PabloIO.cc
 Parallel/SerialTransport.cc
 DataSampling/DataSampling.cc
 DataSampling/ImageDataSampling.cc
 DataSampling/PixonProcessor.cc
 DataSampling/SDDataSampling.cc
 DataSampling/SynDataSampling.cc
 IDL/IDL.cc
 MeasurementComponents/AMueller.cc
 MeasurementComponents/BPoly.cc
 MeasurementComponents/CalCorruptor.cc
 MeasurementComponents/Calibrater.cc
 MeasurementComponents/CalibratingVi2.cc
 MeasurementComponents/CalibratingVi2Factory.cc
 MeasurementComponents/CalSolVi2Organizer.cc
 MeasurementComponents/CEMemImageSkyModel.cc
 MeasurementComponents/ClarkCleanAlgorithm.cc
 MeasurementComponents/ClarkCleanImageSkyModel.cc
 MeasurementComponents/CleanImageSkyModel.cc
 MeasurementComponents/ConvFuncDiskCache.cc
 MeasurementComponents/CSCleanImageSkyModel.cc
 MeasurementComponents/DJones.cc
 MeasurementComponents/EJones.cc
 MeasurementComponents/EPJones.cc
 MeasurementComponents/EVLASwPow.cc
 MeasurementComponents/FJones.cc
 MeasurementComponents/FringeJones.cc
 MeasurementComponents/GlobalFTMachineCallbacks.cc
 MeasurementComponents/GridBoth.cc
 MeasurementComponents/GSpline.cc
 MeasurementComponents/HogbomCleanImageSkyModel.cc
 TransformMachines/IlluminationConvFunc.cc
 MeasurementComponents/ImageSkyModel.cc
 MeasurementComponents/Jones.cc
 MeasurementComponents/KJones.cc
 MeasurementComponents/LJJones.cc
 MeasurementComponents/MakeApproxPSFAlgorithm.cc
 MeasurementComponents/MFCEMemImageSkyModel.cc
 MeasurementComponents/MFCleanImageSkyModel.cc
 MeasurementComponents/MFMSCleanImageSkyModel.cc
 MeasurementComponents/MSCleanImageSkyModel.cc
 MeasurementComponents/MSMetaInfoForCal.cc
 MeasurementComponents/Mueller.cc
 MeasurementComponents/MultiThreadedVisResampler.cc
 MeasurementComponents/NNLSImageSkyModel.cc
 MeasurementComponents/nPBWProjectFT.cc
 MeasurementComponents/PBMosaicFT.cc
 MeasurementComponents/PClarkCleanImageSkyModel.cc
 MeasurementComponents/PixelatedConvFunc.cc
 MeasurementComponents/PredictAlgorithm.cc
 TransformMachines/PSTerm.cc
 MeasurementComponents/PWFCleanImageSkyModel.cc
 MeasurementComponents/ReadMSAlgorithm.cc
 MeasurementComponents/ResidualAlgorithm.cc
 MeasurementComponents/ResamplerWorklet.cc
 MeasurementComponents/SDGrid.cc
 MeasurementComponents/SDPosInterpolator.cc
 MeasurementComponents/SDDoubleCircleGainCalImpl.cc
 MeasurementComponents/SDDoubleCircleGainCal.cc
 MeasurementComponents/SimACohCalc.cc
 MeasurementComponents/SimACoh.cc
 MeasurementComponents/SingleDishSkyCal.cc
 MeasurementComponents/SkyCal.cc
 MeasurementComponents/SolvableVisCal.cc
 MeasurementComponents/SolveDataBuffer.cc
 MeasurementComponents/StandardVisCal.cc
 MeasurementComponents/SteepestDescentSolver.cc
 MeasurementComponents/TsysGainCal.cc
 MeasurementComponents/UVMod.cc
 MeasurementComponents/VisCal.cc
 MeasurementComponents/VisCalGlobals.cc
 MeasurementComponents/VisCalSolver.cc
 MeasurementComponents/VisCalSolver2.cc
 MeasurementComponents/VisVector.cc
 TransformMachines/VisibilityResamplerBase.cc
 TransformMachines/VisibilityResampler.cc
 TransformMachines/VLACalcIlluminationConvFunc.cc
 TransformMachines/VLAIlluminationConvFunc.cc
 MeasurementComponents/WBCleanImageSkyModel.cc
 MeasurementComponents/WFCleanImageSkyModel.cc
 TransformMachines/WOnlyConvFunc.cc
 TransformMachines/WTerm.cc
 MeasurementEquations/CCList.cc
 MeasurementEquations/CEMemModel.cc
 MeasurementEquations/CEMemProgress.cc
 MeasurementEquations/ClarkCleanLatModel.cc
 MeasurementEquations/ClarkCleanModel.cc
 MeasurementEquations/ClarkCleanProgress.cc
 MeasurementEquations/ConvolutionEquation.cc
 MeasurementEquations/CubeSkyEquation.cc
 MeasurementEquations/Deconvolver.cc
 MeasurementEquations/Entropy.cc
 MeasurementEquations/Feather.cc
 MeasurementEquations/Imager.cc
 MeasurementEquations/Imager2.cc
 MeasurementEquations/ImagerMultiMS.cc
 MeasurementEquations/ImageMSCleaner.cc
 MeasurementEquations/ImageNACleaner.cc	
 MeasurementEquations/IncCEMemModel.cc
 MeasurementEquations/IncEntropy.cc
 MeasurementEquations/IPLatConvEquation.cc
 MeasurementEquations/LatConvEquation.cc
 MeasurementEquations/LatticeModel.cc
 MeasurementEquations/LinearMosaic.cc
 MeasurementEquations/MatrixCleaner.cc
 MeasurementEquations/MatrixNACleaner.cc
 MeasurementEquations/MultiTermMatrixCleaner.cc
 MeasurementEquations/Simulator.cc
 MeasurementEquations/SkyEquation.cc
 MeasurementEquations/StokesUtil2.cc
 MeasurementEquations/VisEquation.cc
 MeasurementEquations/VPManager.cc
 TransformMachines/ALMAAperture.cc
 TransformMachines/ALMABeamCalcParams.cc
 TransformMachines/ALMACalcIlluminationConvFunc.cc
 Parallel/Applicator.cc
 Parallel/MPIError.cc
 Parallel/MPITransport.cc
 Parallel/PabloIO.cc
 Parallel/SerialTransport.cc
 Utilities/AppRC.cc		
 Utilities/FFT2D.cc	
 Utilities/FixVis.cc
 Utilities/SigHandler.cc
 Utilities/ThreadCoordinator.cc
 fortran/fpbmos.f	
 fortran/fpbwproj.f	
 fortran/leakantso.f
 ImagerObjects/SynthesisImager.cc
 ImagerObjects/SynthesisImagerVi2.cc
 ImagerObjects/SIImageStore.cc
 ImagerObjects/SIImageStoreMultiTerm.cc
 ImagerObjects/SIMapperCollection.cc
 ImagerObjects/SIMapper.cc
 ImagerObjects/SIMapperImageMosaic.cc
 ImagerObjects/SynthesisIterBot.cc
 ImagerObjects/SIMinorCycleController.cc
 ImagerObjects/SIIterBot.cc
 ImagerObjects/SynthesisDeconvolver.cc
 ImagerObjects/SDAlgorithmBase.cc
 ImagerObjects/SDAlgorithmHogbomClean.cc
 ImagerObjects/SDAlgorithmMSMFS.cc
 ImagerObjects/SDAlgorithmMSClean.cc
 ImagerObjects/SDAlgorithmClarkClean.cc
 ImagerObjects/SDAlgorithmClarkClean2.cc
 ImagerObjects/SDAlgorithmMEM.cc
 ImagerObjects/SDAlgorithmAAspClean.cc
 ImagerObjects/SDMaskHandler.cc
 ImagerObjects/SynthesisNormalizer.cc
 ImagerObjects/SynthesisUtilMethods.cc
 ImagerObjects/DistributedSynthesisIterBot.cc
 ImagerObjects/DistSIIterBot.cc
 ImagerObjects/ParallelImagerFactory.cc
# ImagerObjects2/SynthesisImager.cc
# ImagerObjects2/SIMapperCollection.cc
# ImagerObjects2/SIMapper.cc
# ImagerObjects2/SIMapperImageMosaic.cc
 ImagerObjects/InteractiveMasking.cc
 Utilities/PointingDirectionCalculator.cc
 Utilities/PointingDirectionProjector.cc
 Utilities/SingleDishBeamUtil.cc
 ${BISON_CalLibraryGram_OUTPUTS}
 ${FLEX_CalLibraryGram_OUTPUTS}
  )

install (FILES
	CalTables/BJonesDesc.h
	CalTables/BJonesMBuf.h
	CalTables/BJonesMCol.h
	CalTables/BJonesMRec.h
	CalTables/BJonesTable.h
	CalTables/CLPatchPanel.h
	CalTables/CTColumns.h
	CalTables/CTDesc.h
	CalTables/CTEnums.h
	CalTables/CTInterface.h
#	CalTables/CTSelection.h
	CalTables/CTMainColInterface.h
	CalTables/CTIter.h
	CalTables/CTMainColumns.h
	CalTables/CTMainRecord.h
	CalTables/CTPatchedInterp.h
	CalTables/CTTimeInterp1.h
	CalTables/CalBuffer.h
	CalTables/CalDescBuffer.h
	CalTables/CalDescColumns.h
	CalTables/CalDescColumns2.h
	CalTables/CalDescRecord.h
	CalTables/CalHistRecord.h
	CalTables/CalHistoryBuffer.h
	CalTables/CalHistoryColumns.h
	CalTables/CalInterp.h
	CalTables/CalInterpolation.h
	CalTables/CalInterpolator.h
	CalTables/CalIntpMatch.h
	CalTables/CalIter.h
	CalTables/CalIterBase.h
	CalTables/CalMainBuffer.h
	CalTables/CalMainColumns.h
	CalTables/CalMainColumns2.h
	CalTables/CalMainRecord.h
	CalTables/CalSet.h
	CalTables/CalSetMetaInfo.h
	CalTables/CalTable.h
	CalTables/CalTable2.h
	CalTables/CalTableDesc.h
	CalTables/CalTableDesc2.h
	CalTables/CalTableFromAIPS.h
	CalTables/EPointDesc.h
	CalTables/EPointMBuf.h
	CalTables/EPointMCol.h
	CalTables/EPointTable.h
	CalTables/EPointVJMRec.h
	CalTables/FVisJonesDesc.h
	CalTables/FVisJonesMRec.h
	CalTables/GJonesDesc.h
	CalTables/GJonesMBuf.h
	CalTables/GJonesMCol.h
	CalTables/GJonesTable.h
	CalTables/MJonesDesc.h
	CalTables/MJonesMRec.h
	CalTables/NewCalTable.h
	CalTables/RIorAParray.h
	CalTables/ROCalMainColumns2.h
	CalTables/SkyJonesDesc.h
	CalTables/SolvableCalSetMCol.h
	CalTables/SolvableMJDesc.h
	CalTables/SolvableMJMRec.h
	CalTables/SolvableVJDesc.h
	CalTables/SolvableVJMBuf.h
	CalTables/SolvableVJMCol.h
	CalTables/SolvableVJMRec.h
	CalTables/SolvableVJTable.h
	CalTables/TJonesDesc.h
	CalTables/TJonesMBuf.h
	CalTables/TJonesMCol.h
	CalTables/TJonesTable.h
	CalTables/TimeVarMJDesc.h
	CalTables/TimeVarMJMRec.h
	CalTables/TimeVarVJDesc.h
	CalTables/TimeVarVJMBuf.h
	CalTables/TimeVarVJMCol.h
	CalTables/TimeVarVJMRec.h
	CalTables/TimeVarVJTable.h
	CalTables/VisCalEnum.h
	CalTables/VisJonesDesc.h
	CalTables/VisJonesMBuf.h
	CalTables/VisJonesMCol.h
	CalTables/VisJonesMRec.h
	CalTables/VisJonesTable.h
	CalTables/CalMainColumns2.tcc
	CalTables/CalSet.tcc
	CalTables/ROCalMainColumns2.tcc
	CalTables/SolvableCalSetMCol.tcc
	DESTINATION include/casacode/synthesis/CalTables
	)
install (FILES
    CalLibrary/CalLibraryTools.h
    CalLibrary/CalLibraryParse.h
	DESTINATION include/casacode/synthesis/CalLibrary
    )
install (FILES
	DataSampling/DataSampling.h
	DataSampling/ImageDataSampling.h
	DataSampling/PixonProcessor.h
	DataSampling/SDDataSampling.h
	DataSampling/SynDataSampling.h
	DESTINATION include/casacode/synthesis/DataSampling
	)
install (FILES
	IDL/IDL.h
	DESTINATION include/casacode/synthesis/IDL
	)
install (FILES
	MeasurementComponents/ACoh.h
	MeasurementComponents/AMueller.h
	MeasurementComponents/BPoly.h
	MeasurementComponents/CEMemImageSkyModel.h
	MeasurementComponents/CExp.h
	MeasurementComponents/CExp.new3.h
#	MeasurementComponents/CFDefs.h
	MeasurementComponents/CSCleanImageSkyModel.h
	MeasurementComponents/CalCorruptor.h
	MeasurementComponents/Calibrater.h
	MeasurementComponents/CalibratingVi2.h
	MeasurementComponents/CalibratingVi2Factory.h
	MeasurementComponents/CalSolVi2Organizer.h
	MeasurementComponents/ClarkCleanAlgorithm.h
	MeasurementComponents/ClarkCleanImageSkyModel.h
	MeasurementComponents/CleanImageSkyModel.h
	MeasurementComponents/ConvFuncDiskCache.h
	MeasurementComponents/EJones.h
	MeasurementComponents/EPJones.h
	MeasurementComponents/ExpCache.h
	MeasurementComponents/FJones.h
        MeasurementComponents/FringeJones.h
	MeasurementComponents/GSpline.h
	MeasurementComponents/GlobalFTMachineCallbacks.h
	MeasurementComponents/GridBoth.h
	MeasurementComponents/HogbomCleanImageSkyModel.h
	MeasurementComponents/ImageSkyModel.h
	MeasurementComponents/Jones.h
	MeasurementComponents/KJones.h
	MeasurementComponents/LJJones.h
	MeasurementComponents/MFCEMemImageSkyModel.h
	MeasurementComponents/MFCleanImageSkyModel.h
	MeasurementComponents/MFMSCleanImageSkyModel.h
	MeasurementComponents/MSCleanImageSkyModel.h
        MeasurementComponents/MSMetaInfoForCal.h
	MeasurementComponents/MThWorkIDEnum.h
	MeasurementComponents/MakeApproxPSFAlgorithm.h
	MeasurementComponents/Mueller.h
	MeasurementComponents/MultiThreadedVisResampler.h
	MeasurementComponents/NNLSImageSkyModel.h
	MeasurementComponents/PBMosaicFT.h
	MeasurementComponents/PClarkCleanImageSkyModel.h
	MeasurementComponents/PWFCleanImageSkyModel.h
	MeasurementComponents/PixelatedConvFunc.h
	MeasurementComponents/PredictAlgorithm.h
	MeasurementComponents/ReadMSAlgorithm.h
	MeasurementComponents/ResamplerWorklet.h
	MeasurementComponents/ResidualAlgorithm.h
	MeasurementComponents/SDGrid.h
	MeasurementComponents/SDPosInterpolator.h
	MeasurementComponents/SDDoubleCircleGainCalImpl.h
	MeasurementComponents/SDDoubleCircleGainCal.h
	MeasurementComponents/SimACoh.h
	MeasurementComponents/SimACohCalc.h
	MeasurementComponents/SingleDishSkyCal.h
	MeasurementComponents/SkyModel.h
	MeasurementComponents/SolvableVisCal.h
	MeasurementComponents/SolveDataBuffer.h
	MeasurementComponents/StandardVisCal.h
	MeasurementComponents/SteepestDescentSolver.h
	MeasurementComponents/TabulatedConvFunc.h
	MeasurementComponents/TsysGainCal.h
	MeasurementComponents/UVMod.h
	MeasurementComponents/VisCal.h
	MeasurementComponents/VisCalGlobals.h
	MeasurementComponents/VisCalSolver.h
	MeasurementComponents/VisCalSolver2.h
	MeasurementComponents/VisVector.h
	MeasurementComponents/WBCleanImageSkyModel.h
	MeasurementComponents/WFCleanImageSkyModel.h
	MeasurementComponents/WOnlyProjectFT.h
	MeasurementComponents/XCorr.h
	MeasurementComponents/nPBWProjectFT.h
	MeasurementComponents/rGridFT.h
	MeasurementComponents/ImageSkyModel.tcc
	DESTINATION include/casacode/synthesis/MeasurementComponents
	)
install (FILES
	MeasurementEquations/ArrayModel.h
	MeasurementEquations/CCList.h
	MeasurementEquations/CEMemModel.h
	MeasurementEquations/CEMemProgress.h
	MeasurementEquations/ClarkCleanLatModel.h
	MeasurementEquations/ClarkCleanModel.h
	MeasurementEquations/ClarkCleanProgress.h
	MeasurementEquations/ConvolutionEquation.h
	MeasurementEquations/CubeSkyEquation.h
	MeasurementEquations/Deconvolver.h
	MeasurementEquations/Entropy.h
	MeasurementEquations/HogbomCleanModel.h
	MeasurementEquations/IPLatConvEquation.h
	MeasurementEquations/ImageMSCleaner.h
	MeasurementEquations/ImageNACleaner.h
	MeasurementEquations/Imager.h
	MeasurementEquations/ImagerMultiMS.h
	MeasurementEquations/IncCEMemModel.h
	MeasurementEquations/IncEntropy.h
	MeasurementEquations/Iterate.h
	MeasurementEquations/LatConvEquation.h
	MeasurementEquations/LatticeModel.h
	MeasurementEquations/LinearEquation.h
	MeasurementEquations/LinearModel.h
	MeasurementEquations/LinearMosaic.h
	MeasurementEquations/MaskedArrayModel.h
	MeasurementEquations/MaskedHogbomCleanModel.h
	MeasurementEquations/MatrixCleaner.h
	MeasurementEquations/MatrixNACleaner.h
	MeasurementEquations/MultiTermMatrixCleaner.h
	MeasurementEquations/ResidualEquation.h
	MeasurementEquations/Simulator.h
	MeasurementEquations/SkyEquation.h
	MeasurementEquations/StokesUtil.h
	MeasurementEquations/VPManager.h
	MeasurementEquations/VisEquation.h
	MeasurementEquations/ArrayModel.tcc
	MeasurementEquations/HogbomCleanModel.tcc
	MeasurementEquations/LinearEquation.tcc
	MeasurementEquations/LinearModel.tcc
	MeasurementEquations/MaskedArrayModel.tcc
	MeasurementEquations/MaskedHogbomCleanModel.tcc
	MeasurementEquations/ResidualEquation.tcc
	MeasurementEquations/StokesUtil.tcc
	DESTINATION include/casacode/synthesis/MeasurementEquations
	)
install (FILES
	ImagerObjects/SynthesisImager.h
	ImagerObjects/SynthesisImagerVi2.h
	ImagerObjects/SIImageStore.h
	ImagerObjects/SIImageStoreMultiTerm.h
	ImagerObjects/SIMapperCollection.h
	ImagerObjects/SIMapper.h
	ImagerObjects/SIMapperImageMosaic.h
	ImagerObjects/SynthesisIterBot.h
	ImagerObjects/SIMinorCycleController.h
	ImagerObjects/SIIterBot.h
	ImagerObjects/SynthesisDeconvolver.h
	ImagerObjects/SDMaskHandler.h
	ImagerObjects/SynthesisNormalizer.h
	ImagerObjects/SynthesisUtilMethods.h
        ImagerObjects/SynthesisNormalizer.h
        ImagerObjects/SynthesisUtilMethods.h
        ImagerObjects/ContinuumPartitionMixin.h
        ImagerObjects/CubePartitionMixin.h
        ImagerObjects/DistributedSynthesisIterBot.h
        ImagerObjects/DistSIIterBot.h
        ImagerObjects/IterationControl.h
        ImagerObjects/MultiParamFieldIterator.h
        ImagerObjects/ParallelImager.h
        ImagerObjects/ParallelImagerAdaptor.h
        ImagerObjects/ParallelImagerFactory.h
        ImagerObjects/ParallelImagerMixin.h
        ImagerObjects/ParallelImagerParams.h
        ImagerObjects/ParamFieldIterator.h
        ImagerObjects/SerialPartitionMixin.h
        ImagerObjects/SynthesisDeconvolverMixin.h
        ImagerObjects/SynthesisImagerMixin.h
        ImagerObjects/SynthesisNormalizerMixin.h
	ImagerObjects/SDAlgorithmBase.h
	ImagerObjects/SDAlgorithmHogbomClean.h
	ImagerObjects/SDAlgorithmMSMFS.h
	ImagerObjects/SDAlgorithmMSClean.h
	ImagerObjects/SDAlgorithmClarkClean.h
	ImagerObjects/SDAlgorithmClarkClean2.h
	ImagerObjects/SDAlgorithmMEM.h
	ImagerObjects/SDAlgorithmAAspClean.h
	ImagerObjects/InteractiveMasking.h
        ImagerObjects/MPIGlue.h
	DESTINATION include/casacode/synthesis/ImagerObjects
	)
install (FILES
	Parallel/Algorithm.h
	Parallel/Applicator.h
	Parallel/MPIError.h
	Parallel/PTransport.h
	Parallel/PabloIO.h
	DESTINATION include/casacode/synthesis/Parallel
	)
install (FILES 
	TransformMachines2/ATerm.h
	TransformMachines2/AWConvFuncEPJones.h
	TransformMachines2/AWConvFunc.h
	TransformMachines2/AWProjectFT.h
	TransformMachines2/AWProjectWBFT.h
	TransformMachines2/AWProjectWBFTNew.h
	TransformMachines2/AWVisResampler.h
	TransformMachines2/AzElAperture.h
	TransformMachines2/BeamSkyJones.h
	TransformMachines2/CFBuffer.h
	TransformMachines2/CFCache.h
	TransformMachines2/CFDefs.h
	TransformMachines2/CFStore.h
	TransformMachines2/CFStore2.h
	TransformMachines2/CFTerms.h
	TransformMachines2/ComponentFTMachine.h
	TransformMachines2/ConvolutionFunction.h
	TransformMachines2/EVLAAperture.h
	TransformMachines2/EVLAConvFunc.h
	TransformMachines2/FortranizedLoops.h
	TransformMachines2/GridFT.h
	TransformMachines2/HetArrayConvFunc.h
	TransformMachines2/IlluminationConvFunc.h
	TransformMachines2/FTMachine.h
	TransformMachines2/MosaicFT.h
	TransformMachines2/MosaicFTNew.h	
        TransformMachines2/MultiTermFTNew.h
	TransformMachines2/NoOpATerm.h
	TransformMachines2/PolOuterProduct.h
	TransformMachines2/PSTerm.h
	TransformMachines2/SetJyGridFT.h	
	TransformMachines2/SimpleComponentFTMachine.h
	TransformMachines2/SimplePBConvFunc.h
	TransformMachines2/SkyJones.h
	TransformMachines2/TabulatedConvFunc.h
	TransformMachines2/Utils.h
	TransformMachines2/VBStore.h
	TransformMachines2/VisibilityResamplerBase.h
	TransformMachines2/VisibilityResampler.h
	TransformMachines2/VisModelData.h
	TransformMachines2/VLACalcIlluminationConvFunc.h
	TransformMachines2/VLAIlluminationConvFunc.h
        TransformMachines2/VPSkyJones.h
	TransformMachines2/WPConvFunc.h
	TransformMachines2/WProjectFT.h
	TransformMachines2/WTerm.h
	DESTINATION include/casacode/synthesis/TransformMachines2
       )
install (FILES
	TransformMachines/BeamCalc.h
	TransformMachines/BeamSkyJones.h
	TransformMachines/BeamSquint.h
	TransformMachines/CFCache.h
	TransformMachines/CFDefs.h
	TransformMachines/CFStore.h
	TransformMachines/CFStore2.h
	TransformMachines/CFBuffer.h
	TransformMachines/CFCell.h
	TransformMachines/PolOuterProduct.h
	TransformMachines/ComponentFTMachine.h
	TransformMachines/ConvolutionFunction.h
	TransformMachines/DBeamSkyJones.h
	TransformMachines/CFTerms.h
	TransformMachines/PSTerm.h
	TransformMachines/WTerm.h
	TransformMachines/FTMachine.h
	TransformMachines/FTMachine.tcc
	TransformMachines/GridFT.h
	TransformMachines/SetJyGridFT.h
	TransformMachines/HetArrayConvFunc.h
	TransformMachines/MosaicFT.h
	TransformMachines/MosaicFTNew.h
	TransformMachines/MultiTermFT.h
	TransformMachines/MultiTermFTNew.h
	TransformMachines/NewMultiTermFT.h
	TransformMachines/PBMath.h
	TransformMachines/PBMath1D.h
	TransformMachines/PBMath1DAiry.h
	TransformMachines/PBMath1DCosPoly.h
	TransformMachines/PBMath1DEVLA.h
	TransformMachines/PBMath1DGauss.h
	TransformMachines/PBMath1DIPoly.h
	TransformMachines/PBMath1DNumeric.h
	TransformMachines/PBMath1DPoly.h
	TransformMachines/PBMath2D.h
	TransformMachines/PBMath2DImage.h
	TransformMachines/PBMathInterface.h
	TransformMachines/SimpCompGridMachine.h
	TransformMachines/SimpComponentGridMachine.h
	TransformMachines/SimpleComponentFTMachine.h
	TransformMachines/SimplePBConvFunc.h
	TransformMachines/SkyJones.h
	TransformMachines/StokesImageUtil.h
	TransformMachines/SynthesisError.h
	TransformMachines/Utils.h
	TransformMachines/VPSkyJones.h
	TransformMachines/VisModelData.h
	TransformMachines/WPConvFunc.h
	TransformMachines/WProjectFT.h
        TransformMachines/ATerm.h
        TransformMachines/NoOpATerm.h
#        TransformMachines/AWConvFunc2.h
        TransformMachines/AWConvFuncEPJones.h
        TransformMachines/AWProjectFT.h
        TransformMachines/AWProjectWBFT.h
        TransformMachines/AWProjectWBFTNew.h
	TransformMachines/AWVisResampler.h
#	TransformMachines/ProtoVR.h
#	TransformMachines/cDataToGridImpl.h
	TransformMachines/AzElAperture.h
	TransformMachines/EVLAAperture.h
	TransformMachines/EVLAConvFunc.h
	TransformMachines/IlluminationConvFunc.h
	TransformMachines/VBStore.h
	TransformMachines/VLACalcIlluminationConvFunc.h
	TransformMachines/VLAIlluminationConvFunc.h
	TransformMachines/VisibilityResampler.h
	TransformMachines/VisibilityResamplerBase.h
	TransformMachines/WOnlyConvFunc.h
	TransformMachines/ALMAAperture.h
	TransformMachines/ALMACalcIlluminationConvFunc.h
	DESTINATION include/casacode/synthesis/TransformMachines
	)
install (FILES
	Utilities/AppRC.h
        Utilities/FFT2D.h
	Utilities/FixVis.h
	Utilities/SigHandler.h 
	Utilities/ThreadCoordinator.h
	Utilities/PointingDirectionCalculator.h
	Utilities/PointingDirectionProjector.h
	Utilities/SingleDishBeamUtil.h
	DESTINATION include/casacode/synthesis/Utilities
	)
casa_add_executable( synthesis casasplit apps/casasplit/casasplit.cc )
casa_add_executable( synthesis imageconcat apps/utils/imageconcat.cc )
casa_add_assay( synthesis ImagerObjects/test/tSIIterBot.cc )
casa_add_assay( synthesis ImagerObjects/test/tSynthesisUtils.cc )
casa_add_assay( synthesis TransformMachines2/test/tVisModelDataRefim.cc )
casa_add_demo ( synthesis TransformMachines/test/dImagingWeightViaGridFT.cc )
casa_add_assay( synthesis TransformMachines/test/tVisModelData.cc )
casa_add_assay( synthesis TransformMachines/test/tStokesImageUtil.cc )
#casa_add_assay( synthesis TransformMachines/test/tCFCache.cc )
#casa_add_assay( synthesis TransformMachines/test/tCImageRotation.cc )
#casa_add_assay( synthesis TransformMachines/test/tInitMaps.cc )
#casa_add_assay( synthesis TransformMachines/test/tAWP.cc )
casa_add_assay( synthesis DataSampling/test/tPixonProcessor.cc )
casa_add_assay( synthesis IDL/test/tIDL.cc )
casa_add_assay( synthesis MeasurementComponents/test/tALMAAperture.cc )
casa_add_assay( synthesis MeasurementComponents/test/tEVLAAperture.cc )
casa_add_assay( synthesis MeasurementComponents/test/tAlgoPClark.cc )
casa_add_assay( synthesis MeasurementComponents/test/tBeamSquint.cc )
casa_add_assay( synthesis MeasurementComponents/test/tCalibrater.cc )
casa_add_assay( synthesis MeasurementComponents/test/tFJones.cc )
casa_add_assay( synthesis MeasurementComponents/test/tKJones.cc )
casa_add_assay( synthesis MeasurementComponents/test/tPBMath.cc )
casa_add_assay( synthesis MeasurementComponents/test/tPBMath2D.cc )
casa_add_assay( synthesis MeasurementComponents/test/tPBTable.cc )
#casa_add_assay( synthesis MeasurementComponents/test/tTrVI2.cc )
casa_add_assay( synthesis MeasurementComponents/test/tVPSkyJones.cc )
casa_add_demo ( synthesis MeasurementEquations/test/dCEMemModel.cc )
casa_add_assay( synthesis MeasurementEquations/test/tCCList.cc )
casa_add_assay( synthesis MeasurementEquations/test/tCEMemModel.cc )
casa_add_assay( synthesis MeasurementEquations/test/tClarkCleanLatModel.cc )
casa_add_assay( synthesis MeasurementEquations/test/tClarkCleanModel.cc )
casa_add_assay( synthesis MeasurementEquations/test/tConvolutionEquation.cc )
casa_add_assay( synthesis MeasurementEquations/test/tFeather.cc )
casa_add_assay( synthesis MeasurementEquations/test/tImager.cc )
casa_add_assay( synthesis MeasurementEquations/test/tIncCEMemModel.cc )
casa_add_assay( synthesis MeasurementEquations/test/tLatConvEquation.cc )
casa_add_assay( synthesis MeasurementEquations/test/tStokesUtil.cc )
casa_add_assay( synthesis Parallel/test/tApplicator.cc )
casa_add_assay( synthesis CalTables/test/tCalInterpolation.cc )
casa_add_assay( synthesis CalTables/test/tCalIntpMatch.cc )
casa_add_assay( synthesis CalTables/test/tNewCalTable.cc )
casa_add_assay( synthesis CalTables/test/tCTIter.cc )
casa_add_assay( synthesis CalTables/test/tRIorAPArray.cc )
casa_add_assay( synthesis CalTables/test/tCLPatchPanel.cc )
casa_add_assay( synthesis CalTables/test/tCTTimeInterp1.cc )
#casa_add_assay( synthesis CalTables/test/tCTPatchedInterp.cc )
#casa_add_assay( synthesis CalTables/test/tCalTables.cc )
casa_add_assay( synthesis CalTables/test/tCTSelection.cc )
casa_add_assay( synthesis CalTables/test/tCTGenericFill.cc )


casa_add_test( synthesis CalLibrary/test/tCalLibraryParse.cc )
casa_add_unit_test( MODULES synthesis SOURCES TransformMachines2/test/tAWPFTM.cc TransformMachines2/test/MakeMS.cc ) 
casa_add_unit_test( MODULES synthesis SOURCES TransformMachines2/test/tFTMachine.cc TransformMachines2/test/MakeMS.cc ) 
casa_add_unit_test( MODULES synthesis SOURCES TransformMachines/test/tGridFT.cc TransformMachines2/test/MakeMS.cc )
casa_add_unit_test( MODULES synthesis SOURCES TransformMachines/test/tPBMath1DEVLA.cc  ) 
casa_add_unit_test( MODULES synthesis SOURCES ImagerObjects/test/tSynthesisImager.cc  TransformMachines2/test/MakeMS.cc )
casa_add_unit_test( MODULES synthesis SOURCES ImagerObjects/test/tSynthesisImagerVi2.cc  TransformMachines2/test/MakeMS.cc )
casa_add_unit_test( MODULES synthesis SOURCES Utilities/test/tFFT2D.cc  ) 
casa_add_unit_test( MODULES synthesis SOURCES CalTables/test/tCTPatchedInterp.cc )
casa_add_unit_test( MODULES synthesis SOURCES ImagerObjects/test/tLabelandFindRegions.cc )


casa_add_google_test( MODULES mstransform SOURCES ../mstransform/MSTransform/test/tMSTransformIterator.cc  ../mstransform/TVI/test/TestUtilsTVI.cc)
casa_add_google_test( MODULES mstransform SOURCES ../mstransform/TVI/test/tChannelAverageTVI.cc  ../mstransform/TVI/test/TestUtilsTVI.cc)
casa_add_google_test( MODULES mstransform SOURCES ../mstransform/TVI/test/tHanningSmoothTVI.cc  ../mstransform/TVI/test/TestUtilsTVI.cc)
casa_add_google_test( MODULES mstransform SOURCES ../mstransform/TVI/test/tPhaseShiftingTVI.cc  ../mstransform/TVI/test/TestUtilsTVI.cc)
#casa_add_google_test( MODULES mstransform SOURCES ../mstransform/TVI/test/tStatWtTVI.cc  ../mstransform/TVI/test/TestUtilsTVI.cc)
casa_add_google_test( NOT_ON_APPLE MODULES mstransform SOURCES ../mstransform/TVI/test/tRegriddingTVI.cc  ../mstransform/TVI/test/TestUtilsTVI.cc)
casa_add_google_test( NOT_ON_APPLE MODULES mstransform SOURCES ../mstransform/TVI/test/tUVContSubTVI.cc  ../mstransform/TVI/test/TestUtilsTVI.cc)

casa_add_google_test( MODULES synthesis SOURCES MeasurementComponents/test/tCalibraterSolve_GT.cc )
casa_add_google_test( MODULES synthesis SOURCES MeasurementComponents/test/tCalibraterSolveSimData_GT.cc )
casa_add_google_test( MODULES synthesis SOURCES MeasurementComponents/test/tCalSolVi2Organizer_GT.cc )
casa_add_google_test( MODULES synthesis SOURCES MeasurementComponents/test/tRecursiveVi2LayersWithCal_GT.cc )
casa_add_google_test( MODULES synthesis SOURCES MeasurementComponents/test/tDJones_GT.cc )
casa_add_google_test( MODULES synthesis SOURCES MeasurementComponents/test/tFringeJones_GT.cc )
casa_add_google_test( MODULES synthesis SOURCES MeasurementComponents/test/tGlinXphJones_GT.cc )
casa_add_google_test( MODULES synthesis SOURCES MeasurementComponents/test/tKJones_GT.cc )
casa_add_google_test( MODULES synthesis SOURCES MeasurementComponents/test/tMMueller_GT.cc )
casa_add_google_test( MODULES synthesis SOURCES MeasurementComponents/test/tMSMetaInfoForCal_GT.cc )
casa_add_google_test( MODULES synthesis SOURCES MeasurementComponents/test/tPJones_GT.cc )
casa_add_google_test( MODULES synthesis SOURCES MeasurementComponents/test/tVisVectorJonesMueller_GT.cc )
casa_add_google_test( MODULES synthesis SOURCES MeasurementComponents/test/tVisCal_GT.cc )
casa_add_google_test( MODULES synthesis SOURCES MeasurementComponents/test/tGJones_GT.cc )
casa_add_google_test( MODULES synthesis SOURCES MeasurementComponents/test/tVisCalGlobals_GT.cc )
casa_add_google_test( MODULES synthesis SOURCES MeasurementComponents/test/tSolveDataBuffer_GT.cc )
casa_add_google_test( MODULES synthesis SOURCES MeasurementComponents/test/SingleDishSkyCal_GTest.cc )

casa_add_google_test( MODULES synthesis SOURCES ImagerObjects/test/SDMaskHandler_GTest.cc )
casa_add_google_test( MODULES synthesis SOURCES MeasurementComponents/test/SDPosInterpolator_GTest.cc )
casa_add_google_test( MODULES synthesis SOURCES MeasurementComponents/test/SDDoubleCircleGainCalImpl_GTest.cc )

