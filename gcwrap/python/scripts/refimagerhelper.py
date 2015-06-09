import os
import commands
import math
import shutil
import string
import time
import re;
from taskinit import *
import copy
#from simple_cluster import simple_cluster

'''
A set of helper functions for the tasks  tclean, xxxx

Summary...

    
'''

debug = False

#############################################
#############################################

#############################################
class PySynthesisImager:

    def __init__(self,params):
        ################ Tools
        self.initDefaults()

        # Check all input parameters, after partitioning setup.

        # Selection Parameters. Dictionary of dictionaries, indexed by 'ms0','ms1',...
        self.allselpars = params.getSelPars()
        # Imaging/Deconvolution parameters. Same for serial and parallel runs
        self.alldecpars = params.getDecPars()
        self.allimpars = params.getImagePars()
        self.allgridpars = params.getGridPars()
        self.allnormpars = params.getNormPars()
        self.weightpars = params.getWeightPars()
        # Iteration parameters
        self.iterpars = params.getIterPars() ## Or just params.iterpars

        # CFCache params
        self.cfcachepars = params.getCFCachePars()
        ## Number of fields ( main + outliers )
        self.NF = len(self.allimpars.keys())
        self.stopMinor = {}  ##[0]*self.NF
        for immod in range(0,self.NF):
            self.stopMinor[str(immod)]=0
        ## Number of nodes. This gets set for parallel runs
        ## It can also be used serially to process the major cycle in pieces.
        self.NN = 1 

#        isvalid = self.checkParameters()
#        if isvalid==False:
#            print 'Invalid parameters'

#############################################
#    def checkParameters(self):
#        # Copy the imagename from impars to decpars, for each field.
#        for immod in range(0,self.NF):
#            self.alldecpars[str(immod)]['imagename'] = self.allimpars[str(immod)]['imagename']
#        return True

#############################################
    def makeCFCache(self,exists):
        # Make the CFCache and re-load it.  The following calls beomce
        # NoOps (in SynthesisImager.cc) if the gridder is not one
        # which uses CFCache.
        if (exists):
            print "CFCache already exists";
        else:
            self.dryGridding();
            self.fillCFCache();
            self.reloadCFCache();
        
#############################################
    def initializeImagers(self):
        
        ## Initialize the tool for the current node
        self.SItool = casac.synthesisimager()
        
        ## Send in selection parameters for all MSs in the list.
        for mss in sorted( (self.allselpars).keys() ):
            self.SItool.selectdata( self.allselpars[mss] )
#            self.SItool.selectdata( **(self.allselpars[mss]) )

        ## For each image-field, define imaging parameters
#        nimpars = copy.deepcopy(self.allimpars)
#        for fld in range(0,self.NF):
#            self.SItool.defineimage( **( nimpars[str(fld)]  ) )
        
        # If cfcache directory already exists, assume that it is
        # usable and is correct.  makeCFCache call then becomes a
        # NoOp.
        cfCacheName=self.allgridpars['0']['cfcache'];
        exists = (os.path.exists(cfCacheName) and os.path.isdir(cfCacheName));

        for fld in range(0,self.NF):
            self.SItool.defineimage( self.allimpars[str(fld)] , self.allgridpars[str(fld)] )


        self.makeCFCache(exists);

#############################################

    def initializeDeconvolvers(self):
         for immod in range(0,self.NF):
              self.SDtools.append(casac.synthesisdeconvolver())
              self.SDtools[immod].setupdeconvolution(decpars=self.alldecpars[str(immod)])

#############################################
    ## Overloaded by ParallelCont
    def initializeNormalizers(self):
        for immod in range(0,self.NF):
            self.PStools.append(casac.synthesisnormalizer())
            #normpars = {'imagename':self.allimpars[str(immod)]['imagename']}
            #normpars['mtype'] = self.allgridpars[str(immod)]['mtype']
            #normpars['weightlimit'] = self.allgridpars[str(immod)]['weightlimit']
            #normpars['ntaylorterms'] = self.allimpars[str(immod)]['ntaylorterms']
            #normpars['facets'] = self.allgridpars[str(immod)]['facets']
            normpars = self.allnormpars[str(immod)]
            self.PStools[immod].setupnormalizer(normpars=normpars)

#############################################

    def initializeIterationControl(self):
        self.IBtool = casac.synthesisiterbot()
        itbot = self.IBtool.setupiteration(iterpars=self.iterpars)

#############################################

    def restoreImages(self):
         for immod in range(0,self.NF):
              self.SDtools[immod].restore()

#############################################

    def getSummary(self,fignum=1):
        summ = self.IBtool.getiterationsummary()
        self.plotReport( summ, fignum )
        return summ

#############################################
    def deleteImagers(self):
        if self.SItool != None:
            self.SItool.done()

    def deleteDeconvolvers(self):
         for immod in range(0,len(self.SDtools)):
              self.SDtools[immod].done()

    def deleteNormalizers(self):
         for immod in range(0,len(self.PStools)):
            self.PStools[immod].done()

    def deleteIterBot(self):
         if self.IBtool != None:
              self.IBtool.done()

    def deleteCluster(self):
#         print 'no cluster to delete'
        return

    def initDefaults(self):
        # Reset globals/members
         self.NF=1
         self.stopMinor={'0':0}  # Flag to call minor cycle for this field or not.
         self.NN=1
         self.SItool=None
         self.SDtools=[]
         self.PStools=[]
         self.IBtool=None
    
#############################################

    def deleteTools(self):
         self.deleteImagers()
         self.deleteDeconvolvers()
         self.deleteNormalizers()
         self.deleteIterBot()
         self.initDefaults()
         self.deleteCluster()

#############################################

    def hasConverged(self):
        # Merge peak-res info from all fields to decide iteration parameters
         for immod in range(0,self.NF):
              initrec =  self.SDtools[immod].initminorcycle() 
              self.IBtool.mergeinitrecord( initrec );
              print "Peak res of field ",immod, " : " ,initrec['peakresidual']
#              casalog.post("["+self.allimpars[str(immod)]['imagename']+"] : Peak residual : %5.5f"%(initrec['peakresidual']), "INFO")

         self.runInteractiveGUI2()

        # Check with the iteration controller about convergence.
         stopflag = self.IBtool.cleanComplete()
         print 'Converged : ', stopflag
         if( stopflag>0 ):
             stopreasons = ['iteration limit', 'threshold', 'force stop']
             casalog.post("Reached global stopping criterion : " + stopreasons[stopflag-1], "INFO")
         return (stopflag>0)

#############################################
    def runInteractiveGUI2(self):
        if self.iterpars['interactive'] == True:
            self.stopMinor = self.IBtool.pauseforinteraction()
            #print "Actioncodes in python : " , self.stopMinor

#############################################
    def runInteractiveGUI(self):
        if self.iterpars['interactive'] == True:
            iterdetails = self.IBtool.getiterationdetails()
            for immod in range(0,self.NF):
                if self.stopMinor[str(immod)]==0 :
                    iterparsmod =  self.SDtools[immod].interactivegui( iterdetails ) 
                    #print 'Input iterpars : ', iterdetails['niter'], iterdetails['cycleniter'], iterdetails['threshold']
                    self.iterpars.update(iterparsmod) 
                    #print 'Output iterpars : ', self.iterpars['niter'],self.iterpars['cycleniter'],self.iterpars['threshold']
                    itbot = self.IBtool.setupiteration(iterpars=self.iterpars)

                    if iterparsmod.has_key('actioncode') :
                        self.stopMinor[str(immod)] = iterparsmod['actioncode']  # 0 or 1 or 2 ( old interactive viewer )

            alldone=True
            for immod in range(0,self.NF):
                alldone = alldone and (self.stopMinor[str(immod)]==2)
            if alldone==True:
                self.IBtool.changestopflag( True )
#            if self.stopMinor==[2]*self.NF:
#                self.IBtool.changestopflag( True )
             #itbot = self.IBtool.setupiteration(iterpars=self.iterpars)

#############################################
    def makePSF(self):

        self.makePSFCore()

        ### Gather PSFs (if needed) and normalize by weight
        for immod in range(0,self.NF):
            self.PStools[immod].gatherpsfweight() 
            self.PStools[immod].dividepsfbyweight()

#############################################

    def runMajorCycle(self):
        for immod in range(0,self.NF):
            self.PStools[immod].dividemodelbyweight()
            self.PStools[immod].scattermodel() 

        if self.IBtool != None:
            lastcycle = (self.IBtool.cleanComplete() > 0)
        else:
            lastcycle = True
        self.runMajorCycleCore(lastcycle)

        if self.IBtool != None:
            self.IBtool.endmajorcycle()
        ### Gather residuals (if needed) and normalize by weight
        for immod in range(0,self.NF):
            self.PStools[immod].gatherresidual() 
            self.PStools[immod].divideresidualbyweight()
            self.PStools[immod].multiplymodelbyweight()

#############################################
    def predictModel(self):
        for immod in range(0,self.NF):
            self.PStools[immod].dividemodelbyweight()
            self.PStools[immod].scattermodel() 

        self.predictModelCore()
##        self.SItool.predictmodel();

#############################################
    def dryGridding(self):
        self.SItool.drygridding(**(self.cfcachepars)) ;
#############################################
## Overloaded for parallel runs
    def fillCFCache(self):
        cfcName = self.allgridpars['0']['cfcache'];
        cflist=[f for f in os.listdir(cfcName) if re.match(r'CFS*', f)];
#        cflist = ["CFS_0_0_CF_1_0_1.im", "CFS_0_0_CF_2_0_0.im", "CFS_0_0_CF_2_0_1.im"];
        self.cfcachepars['cflist']=cflist;

        self.SItool.fillcfcache(**(self.cfcachepars)) ;
#############################################
    def reloadCFCache(self):
        self.SItool.reloadcfcache();

#############################################
## Overloaded for parallel runs
    def setWeighting(self):
        ## Set weighting parameters, and all pars common to all fields.
        self.SItool.setweighting( **(self.weightpars) )
        
 #       print "get set density from python"
 #       self.SItool.getweightdensity()
 #       self.SItool.setweightdensity()

        
#############################################
## Overloaded for parallel runs
    def makePSFCore(self):
        self.SItool.makepsf()
#############################################
## Overloaded for parallel runs
    def runMajorCycleCore(self, lastcycle):
        self.SItool.executemajorcycle(controls={'lastcycle':lastcycle})
#############################################
## Overloaded for parallel runs
    def predictModelCore(self):
        self.SItool.predictmodel()
#############################################

    def runMinorCycle(self):
        # Get iteration control parameters
        iterbotrec = self.IBtool.getminorcyclecontrols()
        ##print "Minor Cycle controls : ", iterbotrec
        # Run minor cycle
        for immod in range(0,self.NF):  
            if self.stopMinor[str(immod)]<2 :
                exrec = self.SDtools[immod].executeminorcycle( iterbotrecord = iterbotrec )
                #print '.... iterdone for ', immod, ' : ' , exrec['iterdone']
                self.IBtool.mergeexecrecord( exrec )

#############################################
    def runMajorMinorLoops(self):
         self.runMajorCycle()
         while ( not self.hasConverged() ):
              self.runMinorCycle()
              self.runMajorCycle()

#############################################

    def plotReport( self, summ={} ,fignum=1 ):
        if not ( summ.has_key('summaryminor') and summ.has_key('summarymajor') and summ.has_key('threshold') and summ['summaryminor'].shape[0]==6 ):
            print 'Cannot make summary plot. Please check contents of the output dictionary from tclean.'
            return summ

        import pylab as pl

        # 0 : iteration number (within deconvolver, per cycle)
        # 1 : peak residual
        # 2 : model flux
        # 3 : cyclethreshold
        # 4 : deconvolver id
        # 5 : subimage id (channel, stokes..)

        pl.ioff()

        pl.figure(fignum)
        pl.clf();
        minarr = summ['summaryminor']

        pl.plot( minarr[0,:] , minarr[1,:] , 'r.-' , label='peak residual' , linewidth=1.5, markersize=8.0)
        pl.plot( minarr[0,:] , minarr[2,:] , 'b.-' , label='model flux' )
        pl.plot( minarr[0,:] , minarr[3,:] , 'g--' , label='cycle threshold' )
        bcols = ['b','g','r','y','c']
        minv=1
        niterdone = len(minarr[4,:])
        maxv=niterdone
        for ind in range(1,niterdone):
            if ( minarr[4,ind-1] != minarr[4,ind] )  or  ind == niterdone-1 :
                maxv = ind
                if ind == niterdone-1:
                    maxv = niterdone
                val = int(minarr[4,ind-1])
                pl.bar(minv, 1.0, maxv-minv, 0.0, color=bcols[val%5], alpha=0.1, linewidth=0)
                minv = ind+1
      
        if len(summ['summarymajor'].shape)==1 and summ['summarymajor'].shape[0]>0 :       
            pl.vlines(summ['summarymajor']+0.5,0,1, label='major cycles', linewidth=2.0)

        pl.hlines( summ['threshold'], 0, summ['iterdone'] , linestyle='dashed' ,label='threshold')
    
        pl.xlabel( 'Iteration Count' )
        pl.ylabel( 'Peak Residual' )

        pl.legend()

        pl.savefig('summaryplot_'+str(fignum)+'.png')
        pl.ion()

        return summ;


#######################################################
#######################################################


#############################################
#############################################
## Parallelize only major cycle.
#############################################
class PyParallelContSynthesisImager(PySynthesisImager):

    def __init__(self,params=None):

         PySynthesisImager.__init__(self,params)

         self.PH = PyParallelImagerHelper()
         self.NN = self.PH.NN
         self.selpars = self.allselpars;
         self.allselpars = self.PH.partitionContDataSelection(self.allselpars)
         # self.allcflist = self.PH.partitionCFCacheList(self.cfcachepars['cflist']);
         # self.allcflist = self.PH.partitionCFCacheList(self.allgridpars['0']);
         self.listOfNodes = self.PH.getNodeList();

#############################################
#############################################
    def initializeImagers(self):

        #
        # The sequence of operations in the method is the following:
        #  1. Start imagers on all nodes
        #  2. Check if cfcache exists
        #  3. If cfcache does not exist
        #       - call setdata() and defineimage() for the imager on the first node
        #       - call dryGridding.  This should b a NoOp for FTMs which are not of the AWProject-class 
        #           This makes an "empty" cfcache
        #  4. call setdata() for images on all nodes
        #  5. If cfcache does not exist, call fillCFCache()
        #       This will fill the "empty" CFCache in parallel
        #  6. call reloadCFCache() on all nodes.
        #  7. Finally also call defineImage() on all nodes.
        
        #PySynthesisImager.initializeImagers(self);

        #--------------------------------------
        #  1. Start imagers on all nodes
        #
        joblist=[]
        #### MPIInterface related changes
        #for node in range(0,self.NN):
        for node in self.listOfNodes:
            ## Initialize the tool for the current node
            self.PH.runcmd("toolsi = casac.synthesisimager()", node)

        #---------------------------------------
        #  2. Check if cfcache exists
        #
        cfCacheName=self.allgridpars['0']['cfcache'];
        cfcExists = (os.path.exists(cfCacheName) and os.path.isdir(cfCacheName));

        #---------------------------------------
        #  3. If cfcache does not exist
        #       - call setdata() and defineimage() for the imager on the first node
        #       - call dryGridding.  This should b a NoOp for FTMs which are not of the AWProject-class 
        #           This makes an "empty" cfcache
        if (not cfcExists):
            nodes=[1];
            for node in nodes:
                for mss in sorted( self.selpars.keys() ):
                    joblist.append( self.PH.runcmd("toolsi.selectdata( "+str(self.selpars[mss])+")", node) )
            self.PH.checkJobs(joblist);

            joblist=[];
            for node in nodes:
                for fld in range(0,self.NF):
                    # for fld in range(0,self.NF):
                    #     self.SItool.defineimage( self.allimpars[str(fld)] , self.allgridpars[str(fld)] )
                    cmd="toolsi.defineimage( impars=" + str( self.allimpars[str(fld)] ) + ", gridpars=" + str( self.allgridpars[str(fld)] )   + ")";
                # print "#!$#!%#!$#@$#@$ ",node," ",cmd;
                    joblist.append( self.PH.runcmd(cmd, node ) );
            self.PH.checkJobs(joblist);

            self.dryGridding();

            #self.deleteImagers();

######################################################################################################################################
        #---------------------------------------
        #  4. call setdata() for images on all nodes
        #
        joblist=[];
        print "################### List of nodes: ",self.listOfNodes;
        for node in self.listOfNodes:
            ## Send in Selection parameters for all MSs in the list
            #### MPIInterface related changes (the -1 in the expression below)
            for mss in sorted( (self.allselpars[str(node-1)]).keys() ):
                joblist.append( self.PH.runcmd("toolsi.selectdata( "+str(self.allselpars[str(node-1)][mss])+")", node) )
        self.PH.checkJobs(joblist);

        #---------------------------------------
        #  5. If cfcache does not exist, call fillCFCache()
        #       This will fill the "empty" CFCache in parallel
        #  6. call reloadCFCache() on all nodes.
        if (not cfcExists):
            self.fillCFCache();
        self.reloadCFCache();


        #---------------------------------------
        #  7. Finally also call defineImage() on all nodes.
        #
        joblist=[];
        for node in self.listOfNodes:
            ## For each image-field, define imaging parameters
            nimpars = copy.deepcopy(self.allimpars)
            #print "nimpars = ",nimpars;
            ngridpars = copy.deepcopy(self.allgridpars)
            for fld in range(0,self.NF):
                if self.NN>1:
                    nimpars[str(fld)]['imagename'] = self.PH.getpath(node) + '/' + nimpars[str(fld)]['imagename']+'.n'+str(node)
###                    nimpars[str(fld)]['imagename'] = self.allnormpars[str(fld)]['workdir'] + '/' + nimpars[str(fld)]['imagename']+'.n'+str(node)
###                    nimpars[str(fld)]['imagename'] = nimpars[str(fld)]['imagename']+'.n'+str(node)

#                    ngridpars[str(fld)]['cfcache'] = ngridpars[str(fld)]['cfcache']+'.n'+str(node)
                    # # Give the same CFCache name to all nodes
                    ngridpars[str(fld)]['cfcache'] = ngridpars[str(fld)]['cfcache'];

                joblist.append( self.PH.runcmd("toolsi.defineimage( impars=" + str( nimpars[str(fld)] ) + ", gridpars=" + str( ngridpars[str(fld)] )   + ")", node ) )
        self.PH.checkJobs(joblist);

#############################################

    def initializeNormalizers(self):
        for immod in range(0,self.NF):
            self.PStools.append(casac.synthesisnormalizer())
            normpars = copy.deepcopy( self.allnormpars[str(immod)] )
            partnames = []
            if(self.NN>1):
#                if not shutil.os.path.exists(normpars['workdir']):
#                    shutil.os.system('mkdir '+normpars['workdir'])
                #### MPIInterface related changes
                #for node in range(0,self.NN):
                for node in self.listOfNodes:
                    onename = self.allimpars[str(immod)]['imagename']+'.n'+str(node)
                    partnames.append( self.PH.getpath(node) + '/' + onename  )
##                    partnames.append( normpars['workdir'] + '/' + onename  )
##                    partnames.append( onename  )
                    self.PH.deletepartimages( self.PH.getpath(node), onename ) # To ensure restarts work properly.
                normpars['partimagenames'] = partnames
            self.PStools[immod].setupnormalizer(normpars=normpars)


#############################################
    def setWeighting(self):

        ## Set weight parameters and accumulate weight density (natural)
        joblist=[];
        for node in self.listOfNodes:
            ## Set weighting pars
            joblist.append( self.PH.runcmd("toolsi.setweighting( **" + str(self.weightpars) + ")", node ) )
        self.PH.checkJobs( joblist )

        ## If only one field, do the get/gather/set of the weight density.
        if self.NF == 1 :   ## Remove after gridded wts appear for all fields correctly (i.e. new FTM).

          if self.weightpars['type'] != 'natural' :  ## For natural, this array isn't created at all.
                                                                       ## Remove when we switch to new FTM
            joblist=[];
            for node in self.listOfNodes:
                joblist.append( self.PH.runcmd("toolsi.getweightdensity()", node ) )
            self.PH.checkJobs( joblist )

           ## gather weightdensity and sum and scatter
            print "******************************************************"
            print " gather and scatter now "
            print "******************************************************"
            for immod in range(0,self.NF):
                self.PStools[immod].gatherweightdensity()
                self.PStools[immod].scatterweightdensity()

           ## Set weight density for each nodel
            joblist=[];
            for node in self.listOfNodes:
                joblist.append( self.PH.runcmd("toolsi.setweightdensity()", node ) )
            self.PH.checkJobs( joblist )



    def deleteImagers(self):
         self.PH.runcmd("toolsi.done()")

    def deleteCluster(self):
         self.PH.takedownCluster()
    
# #############################################
    def dryGridding(self):
        nodes=[1];
        joblist=[];
        for node in nodes:
            dummy=[''];
            cmd = "toolsi.drygridding("+str(dummy)+")";
            joblist.append(self.PH.runcmd(cmd,node));
        self.PH.checkJobs(joblist);

#############################################
    def reloadCFCache(self):
        joblist=[];
        for node in self.listOfNodes:
            cmd = "toolsi.reloadcfcache()";
            joblist.append(self.PH.runcmd(cmd,node));
        self.PH.checkJobs(joblist);
#############################################
    def fillCFCache(self):
        # cflist=[f for f in os.listdir(self.allgridpars['cfcache']) if re.match(r'CFS*', f)];
        # partCFList = 
        allcflist = self.PH.partitionCFCacheList(self.allgridpars['0']);
        print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@";
        print "AllCFList = ",allcflist;
        print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@";

        joblist=[];
        for node in self.listOfNodes:
            #print "#!$#!%#!$#@$#@$ ",allcflist;
            cmd = "toolsi.fillcfcache("+str(allcflist[node])+")";
            print "CMD = ",node," ",cmd;
            joblist.append(self.PH.runcmd(cmd,node));
        self.PH.checkJobs(joblist);

        # Linear code
        # cfcName = self.allgridpars['0']['cfcache'];
        # cflist=[f for f in os.listdir(cfcName) if re.match(r'CFS*', f)];
        # self.cfcachepars['cflist']=cflist;
        # self.SItool.fillcfcache(**(self.cfcachepars)) ;
#############################################
    def makePSFCore(self):
        ### Make PSFs
        joblist=[]
        #### MPIInterface related changes
        #for node in range(0,self.PH.NN):
        for node in self.listOfNodes:
             joblist.append( self.PH.runcmd("toolsi.makepsf()",node) )
        self.PH.checkJobs( joblist ) # this call blocks until all are done.

#############################################

    def runMajorCycleCore(self, lastcycle):
        casalog.post("-----------------------------  Running Parallel Major Cycle ----------------------------","INFO")
        ### Run major cycle
        joblist=[]
        #### MPIInterface related changes
        #for node in range(0,self.PH.NN):
        for node in self.listOfNodes:
             joblist.append( self.PH.runcmd("toolsi.executemajorcycle(controls={'lastcycle':"+str(lastcycle)+"})",node) )
        self.PH.checkJobs( joblist ) # this call blocks until all are done.

#############################################
    def predictModelCore(self):
        joblist=[]
        #### MPIInterface related changes
        #for node in range(0,self.PH.NN):
        for node in self.listOfNodes:
             joblist.append( self.PH.runcmd("toolsi.predictmodel()",node) )
        self.PH.checkJobs( joblist ) # this call blocks until all are done.

#############################################
# Parallelize both the major and minor cycle for Cube imaging
# Run a separate instance of PySynthesisImager on each node.
#### ( later, use the live-object interface of ImStore to reference-break the cubes )
#### For nprocesses > nnodes, run the whole 'clean' loop multiple times. 
#############################################
class PyParallelCubeSynthesisImager():

    def __init__(self,params=None):

        self.params=params

        allselpars = params.getSelPars()
        allimagepars = params.getImagePars()
        self.allgridpars = params.getGridPars()
        self.allnormpars = params.getNormPars()
        self.weightpars = params.getWeightPars()
        self.decpars = params.getDecPars()
        self.iterpars = params.getIterPars()
        alldataimpars={}
         
        self.PH = PyParallelImagerHelper()
        self.NN = self.PH.NN
        self.listOfNodes = self.PH.getNodeList();
        ## Partition both data and image coords the same way.
        #self.allselpars = self.PH.partitionCubeDataSelection(allselpars)
        #self.allimpars = self.PH.partitionCubeDeconvolution(allimagepars)

        # to define final image coordinates, run selecdata and definemage
        self.SItool = casac.synthesisimager()
        #print "allselpars=",allselpars
        for mss in sorted( allselpars.keys() ):
            self.SItool.selectdata( allselpars[mss] )
        for fid in sorted( allimagepars.keys() ):
            self.SItool.defineimage( allimagepars[fid], self.allgridpars[fid] )
            # insert coordsys record in imagepars 
            # partionCubeSelection works per field ...
            allimagepars[fid]['csys'] = self.SItool.getcsys()
            alldataimpars[fid] = self.PH.partitionCubeSelection(allselpars,allimagepars[fid])

        # reorganize allselpars and allimpars for partitioned data        
        synu = casac.synthesisutils()
        self.allselpars={}
        self.allimpars={}
        ###print "self.listOfNodes=",self.listOfNodes
        # Repack the data/image parameters per node
        #  - internally it stores zero-based node ids
        #  
        for ipart in self.listOfNodes:
            # convert to zero-based indexing for nodes
            nodeidx = str(ipart-1)
            selparsPerNode= {nodeidx:{}}
            imparsPerNode= {nodeidx:{}}
            for fid in allimagepars.iterkeys():
                for ky in alldataimpars[fid][nodeidx].iterkeys():
                    selparsPerNode[nodeidx][fid]={}
                    if ky.find('ms')==0:
                        # data sel per field
                        selparsPerNode[nodeidx][fid][ky] = alldataimpars[fid][nodeidx][ky].copy();
                        if alldataimpars[fid][nodeidx][ky]['spw']=='-1':
                            selparsPerNode[nodeidx][fid][ky]['spw']=''

            imparsPerNode[nodeidx][fid] = allimagepars[fid].copy()
            imparsPerNode[nodeidx][fid]['csys'] = alldataimpars[fid][nodeidx]['coordsys'].copy()
            imparsPerNode[nodeidx][fid]['nchan'] = alldataimpars[fid][nodeidx]['nchan']
            imparsPerNode[nodeidx]=synu.updateimpars(imparsPerNode[nodeidx])
            self.allselpars.update(selparsPerNode)
            self.allimpars.update(imparsPerNode)

        #print "self.allimpars IN init>>>> ",self.allimpars

        
        joblist=[]
        #### MPIInterface related changes
        #for node in range(0,self.NN):
        for node in self.listOfNodes:
            joblist.append( self.PH.runcmd("from refimagerhelper import ImagerParameters, PySynthesisImager", node) )
        self.PH.checkJobs( joblist )
            

    def initializeImagers(self):
        #print "self.allimpars IN initImager=====",self.allimpars
        joblist=[]
        #### MPIInterface related changes
        #for node in range(0,self.NN):
        for node in self.listOfNodes:

            joblist.append( self.PH.runcmd("paramList = ImagerParameters()", node) )
            joblist.append( self.PH.runcmd("paramList.setSelPars("+str(self.allselpars[str(node-1)]['0'])+")", node) )
            joblist.append( self.PH.runcmd("paramList.setImagePars("+str(self.allimpars[str(node-1)])+")", node) )
            #joblist.append( self.PH.runcmd("paramList.setGridPars("+str(self.allgridpars[str(node-1)])+")", node) )
            joblist.append( self.PH.runcmd("paramList.setGridPars("+str(self.allgridpars)+")", node) )
            joblist.append( self.PH.runcmd("paramList.setWeightPars("+str(self.weightpars)+")", node) )
            joblist.append( self.PH.runcmd("paramList.setDecPars("+str(self.decpars)+")", node) )
            joblist.append( self.PH.runcmd("paramList.setIterPars("+str(self.iterpars)+")", node) )

            joblist.append( self.PH.runcmd("imager = PySynthesisImager(params=paramList)", node) )

            joblist.append( self.PH.runcmd("imager.initializeImagers()", node) )

        self.PH.checkJobs( joblist )

    def initializeDeconvolvers(self):
        joblist=[]
        #### MPIInterface related changes
        #for node in range(0,self.NN):
        for node in self.listOfNodes:
            joblist.append( self.PH.runcmd("imager.initializeDeconvolvers()", node) )
        self.PH.checkJobs( joblist )

    def initializeNormalizers(self):
        joblist=[]
        #### MPIInterface related changes
        #for node in range(0,self.NN):
        for node in self.listOfNodes:
            joblist.append( self.PH.runcmd("imager.initializeNormalizers()", node) )
        self.PH.checkJobs( joblist )

    def setWeighting(self):

        ## Set weight parameters and accumulate weight density (natural)
        joblist=[];
        for node in self.listOfNodes:
            ## Set weighting pars
            joblist.append( self.PH.runcmd("imager.setWeighting()", node ) )
        self.PH.checkJobs( joblist )


    def initializeIterationControl(self):
        joblist=[]
        #### MPIInterface related changes
        #for node in range(0,self.NN):
        for node in self.listOfNodes:
            joblist.append( self.PH.runcmd("imager.initializeIterationControl()", node) )
        self.PH.checkJobs( joblist )

    def makePSF(self):
        joblist=[]
        #### MPIInterface related changes
        #for node in range(0,self.NN):
        for node in self.listOfNodes:
            joblist.append( self.PH.runcmd("imager.makePSF()", node) )
        self.PH.checkJobs( joblist )

    def runMajorMinorLoops(self):
        joblist=[]
        #### MPIInterface related changes
        #for node in range(0,self.NN):
        for node in self.listOfNodes:
            joblist.append( self.PH.runcmd("imager.runMajorMinorLoops()", node) )
        self.PH.checkJobs( joblist )

    def runMajorCycle(self):
        joblist=[]
        #### MPIInterface related changes
        #for node in range(0,self.NN):
        for node in self.listOfNodes:
            joblist.append( self.PH.runcmd("imager.runMajorCycle()", node) )
        self.PH.checkJobs( joblist )

    def predictModel(self):
        joblist=[]
        #### MPIInterface related changes
        #for node in range(0,self.NN):
        for node in self.listOfNodes:
            joblist.append( self.PH.runcmd("imager.predictmodel()", node) )
        self.PH.checkJobs( joblist )

    def restoreImages(self):
        joblist=[]
        #### MPIInterface related changes
        #for node in range(0,self.NN):
        for node in self.listOfNodes:
            joblist.append( self.PH.runcmd("imager.restoreImages()", node) )
        self.PH.checkJobs( joblist )

    def getSummary(self):
        joblist=[]
        #### MPIInterface related changes
        #for node in range(0,self.NN):
        for node in self.listOfNodes:
            joblist.append( self.PH.runcmd("imager.getSummary("+str(node)+")", node) )
        self.PH.checkJobs( joblist )

    def deleteTools(self):
        joblist=[]
        #### MPIInterface related changes
        #for node in range(0,self.NN):
        for node in self.listOfNodes:
            joblist.append( self.PH.runcmd("imager.deleteTools()", node) )
        self.PH.checkJobs( joblist )

#############################################
#############################################
#############################################

class PyParallelDeconvolver(PySynthesisImager):

    def __init__(self,params):

        PySynthesisImager.__init__(self,params)

        self.PH = PyParallelImagerHelper()
        self.NF = len( allimpars.keys() )
        self.listOfNodes = self.PH.getNodeList();
        #### MPIInterface related changes
        #self.NN = self.PH.NN
        self.NN = len(self.listOfNodes);
        if self.NF != self.NN:
             print 'For now, cannot handle nfields != nnodes. Will implement round robin allocation later.'
             print 'Using only ', self.NN, ' fields and nodes'
             

#############################################
    def initializeDeconvolvers(self):
         joblist=[]
         #### MPIInterface related changes
         #for immod in range(0,self.NF):
         for immod in self.listOfNodes:
              self.PH.runcmd("toolsd = casac.synthesisdeconvolver()", immod )
              joblist.append( self.PH.runcmd("toolsd.setupdeconvolution(decpars="+ str(self.alldecpars[str(immod)]) +")", immod ) )
         self.PH.checkJobs( joblist )

#############################################
    def deleteDeconvolvers(self):
         self.PH.runcmd("toolsd.done()")
              
#############################################
    def restoreImages(self):
         self.PH.runcmdcheck("toolsd.restore()")

#############################################
#############################################

    def hasConverged(self):
        # Merge peak-res info from all fields to decide iteration parameters
        self.PH.runcmdcheck("initrec = toolsd.initminorcycle()")

        #### MPIInterface related changes
        #for immod in range(0,self.NF):
        for immod in self.listOfNodes:
             retrec = self.PH.pullval("initrec", immod )
             self.IBtool.mergeinitrecord( retrec[immod] )
             print "Peak res of field ",immod, " on node ", immod , ": " ,retrec[immod]['peakresidual']
#             casalog.post("["+self.allimpars[str(immod)]['imagename']+"] : Peak residual : %5.5f"%(initrec['peakresidual']), "INFO")

        # Check with the iteration controller about convergence.
        stopflag = self.IBtool.cleanComplete()
        print 'Converged : ', stopflag
        if( stopflag>0 ):
            stopreasons = ['iteration limit', 'threshold', 'force stop']
            casalog.post("Reached global stopping criterion : " + stopreasons[stopflag-1], "INFO")
        return (stopflag>0)


#############################################

    def runMinorCycle(self):
        # Get iteration control parameters
        iterbotrec = self.IBtool.getminorcyclecontrols()
        # Run minor cycle
        self.PH.CL.push( iterbotrec = iterbotrec )

        self.PH.runcmdcheck( "exrec = toolsd.executeminorcycle(iterbotrec)" )

        #### MPIInterface related changes
        #for immod in range(0,self.NF):
        for immod in self.listOfNodes:
             retrec = self.PH.pullval("exrec", immod )
             self.IBtool.mergeexecrecord( retrec[immod] )

#############################################
#############################################



#############################################
###  Parallel Imager Helper.
#############################################
#casalog.post('Using clustermanager from MPIInterface', 'WARN')
from mpi4casa.MPIInterface import MPIInterface as mpi_clustermanager

class PyParallelImagerHelper():

    def __init__(self):

        ############### Cluster Info
         self.CL=None
         self.sc=None
         self.nodeList=None;
         # Initialize cluster, and partitioning.
        ############### Number of nodes to parallelize on

         # self.nodeList gets filled by setupCluster()
         self.NN = self.setupCluster()

    def getNodeList(self):
        return self.nodeList;

#############################################
    def partitionCFCacheList(self,gridPars):

        cflist=[f for f in os.listdir(gridPars['cfcache']) if re.match(r'CFS*', f)];

        nCF = len(cflist);
        nProcs=len(self.nodeList);
        
        print "########################################################"
        print "nCF = ",nCF," nProcs = ",nProcs," NodeList=",self.nodeList;
        print "########################################################"

        #n0=int(nCF/self.NN);
        n0=int(nCF/nProcs);
        if (nProcs > nCF):
            n0 = 1;
        allcfs = {};
        nUsed=0; i=1;
        while (nUsed < nCF):
            m = nUsed+n0;
            if (m > nCF): 
		m=nCF;
            allcfs[i]=cflist[nUsed:m];
	    i=i+1;
            nUsed = m;
        return allcfs;
            
#############################################
## Very rudimentary partitioning - only for tests. The actual code needs to go here.
    def partitionContDataSelection(self,oneselpars={}):

        synu = casac.synthesisutils()
        allselpars =  synu.contdatapartition( oneselpars , self.NN )
        synu.done()

        print 'Partitioned Selection : ', allselpars
        return allselpars

#############################################
## Very rudimentary partitioning - only for tests. The actual code needs to go here.
    def partitionCubeDataSelection(self,oneselpars={}):

        synu = casac.synthesisutils()
        allselpars =  synu.cubedatapartition( oneselpars , self.NN )
        synu.done()

        print 'Partitioned Selection : ', allselpars
        return allselpars

#############################################
    def partitionCubeDeconvolution(self,impars={}):

        synu = casac.synthesisutils()
        allimpars =  synu.cubeimagepartition( impars , self.NN )
        synu.done()

        print 'ImSplit : ', allimpars
        return allimpars

#############################################
    def partitionCubeSelection(self, oneselpars={}, oneimpars={}):
        incsys = oneimpars['csys']
        nchan = oneimpars['nchan']
        synu = casac.synthesisutils()
        allpars = synu.cubedataimagepartition(oneselpars, incsys, self.NN, nchan)
        synu.done()

        #print "Cube Data/Im partitioned selection :", allpars
        return allpars

#############################################
    def setupCluster(self):
        # Initialize cluster
#        if((self.clusterdef != '') and os.path.exists(self.clusterdef)):
#            self.sc=simple_cluster()
#            if(self.sc.get_status()==None):
#                self.sc.init_cluster(self.clusterdef, 'cluster_project')


        # * Terminal: Client logs + Server logs
        # * casapy-<timestamp>.log: Client logs
        # * casapy-<timestamp>.log-server-<rank>-host-<hostname>-pid-<pid>: Server logs 
        mpi_clustermanager.set_log_mode('redirect');

        self.sc=mpi_clustermanager.getCluster()
                
        self.CL=self.sc._cluster
        self.nodeList = self.CL.get_engines();
        numproc=len(self.CL.get_engines())
        numprocperhost=len(self.nodeList)/len(self.nodeList) if (len(self.nodeList) >0 ) else 1

        owd=os.getcwd()
        self.CL.pgc('import os')
        self.CL.pgc('from numpy import array,int32')
        self.CL.pgc('os.chdir("'+owd+'")')
        os.chdir(owd)
        print "Setting up ", numproc, " engines."
        return numproc

#############################################
    def takedownCluster(self):
        # Check that all nodes have returned, before stopping the cluster
         self.checkJobs()
         print 'Ending use of cluster, but not closing it. Call clustermanager.stop_cluster() to close it if needed.'
#         self.sc.stop_cluster()
         self.CL=None
         self.sc=None

#############################################
    # This is a blocking call that will wait until jobs are done.
    def checkJobs(self,joblist=[]):
        #### MPIInterface related changes
        numcpu = len(self.nodeList)
        
        if len(joblist)==0:
             joblist = range(numcpu)
             #for k in range(numcpu):
             for k in self.nodeList:
                 joblist[k-1] = self.CL.odo('casalog.post("node '+str(k)+' has completed its job")', k)

        print 'Blocking for nodes to finish'
        over=False
        while(not over):
            overone=True
            time.sleep(1)
            for k in range(len(joblist)):
                try:
                    overone =  self.CL.check_job(joblist[k],False) and overone
                except Exception,e:
                     raise Exception(e)
            over = overone
        print '...done'

#############################################
    def runcmd(self, cmdstr="", node=-1):
         if node >= 0:
              return self.CL.odo( cmdstr , node)
         else:
              self.CL.pgc( cmdstr )

#############################################
    def runcmdcheck(self, cmdstr):
         joblist=[]
         #### MPIInterface related changes
         #for node in range(0,self.NN):
         for node in self.nodeList:
              joblist.append( self.CL.odo( cmdstr, node ) )
         self.checkJobs( joblist )

#############################################
    def pullval(self, varname="", node=0):
         return self.CL.pull( varname , node )

#############################################
    def getpath(self, node=0):
        enginepath = self.sc.get_engine_store(node)
        if enginepath==None:
            return ""
        else:
            return enginepath
#############################################
    def deletepartimages(self, dirname, imname):
        namelist = shutil.fnmatch.filter( os.listdir(dirname), imname+".*" )
        #print "Deleting : ", namelist, ' from ', dirname, ' starting with ', imname
        for aname in namelist:
            shutil.rmtree( dirname + "/" + aname )
##########################################################################################



######################################################
######################################################
######################################################
######################################################

class ImagerParameters():
    def __init__(self, 

                 ## Data Selection
                 msname='',
                 field='',
                 spw='',
                 timestr='',
                 uvdist='',
                 antenna='',
                 scan='',
                 obs='',
                 state='',
                 datacolumn='corrected',

                 ## Image Definition
                 imagename='', 
                 imsize=[1,1], 
                 cell=[10.0,10.0],
                 phasecenter='',
                 stokes='I',
                 projection='SIN',
                 startmodel='', 

                 ## Spectral Parameters
                 specmode='mfs', 
                 reffreq='',
                 nchan=1, 
                 start='', 
                 width='',
                 outframe='LSRK', 
                 veltype='radio', 
                 restfreq=[''],
                 sysvel='', 
                 sysvelframe='',
                 interpolation='nearest',

                 gridder="standard",
#                 ftmachine='gridft', 
                 facets=1, 

                 wprojplanes=1,

                 aterm=True,
                 psterm=True,
                 mterm=True,
                 wbawp = True,
                 cfcache = "",
                 dopointing = False,
                 dopbcorr = True,
                 conjbeams = True,
                 computepastep =360.0,
                 rotatepastep =360.0,
                 
                 pblimit=0.01,
                 normtype='flatnoise',

                 outlierfile='',
                 overwrite=True,

                 weighting='natural', 
                 robust=0.5,
                 npixels=0,
                 uvtaper=[],

                 niter=0, 
                 cycleniter=0, 
                 loopgain=0.1,
                 threshold='0.0Jy',
                 cyclefactor=1.0,
                 minpsffraction=0.1,
                 maxpsffraction=0.8,
                 interactive=False,

                 deconvolver='hogbom',
                 scales=[],
                 ntaylorterms=1, 
                 restoringbeam=[],
#                 mtype='default',
                 mask='',

#                 usescratch=True,
#                 readonly=True,
                 savemodel="none",

                 workdir='',

                 ## CFCache params
                 cflist=[]
                 ):

        self.defaultKey="0";

        ## Selection params. For multiple MSs, all are lists.
        ## For multiple nodes, the selection parameters are modified inside PySynthesisImager
        self.allselpars = {'msname':msname, 'field':field, 'spw':spw, 'scan':scan,
                           'timestr':timestr, 'uvdist':uvdist, 'antenna':antenna, 'obs':obs,'state':state,
                           'datacolumn':datacolumn,
                           'savemodel':savemodel }
#                           'usescratch':usescratch, 'readonly':readonly}

        ## Imaging/deconvolution parameters
        ## The outermost dictionary index is image field. 
        ## The '0' or main field's parameters come from the task parameters
        ## The outlier '1', '2', ....  parameters come from the outlier file
        self.outlierfile = outlierfile
        ## Initialize the parameter lists with the 'main' or '0' field's parameters
        ######### Image definition
        self.allimpars = { self.defaultKey :{'imagename':imagename, 'nchan':nchan, 'imsize':imsize, 
                                 'cell':cell, 'phasecenter':phasecenter, 'stokes': stokes,
                                 'specmode':specmode, 'start':start, 'width':width, 'veltype':veltype,
                                 'ntaylorterms':ntaylorterms,'restfreq':restfreq, 
                                 'outframe':outframe, 'reffreq':reffreq, 'sysvel':sysvel, 'sysvelframe':sysvelframe,
                                 'projection':projection,
                                 'overwrite':overwrite, 'startmodel':startmodel,}    }
        ######### Gridding
        self.allgridpars = { self.defaultKey :{'gridder':gridder,
                                   'aterm': aterm, 'psterm':psterm, 'mterm': mterm, 'wbawp': wbawp, 
                                   'cfcache': cfcache,'dopointing':dopointing, 'dopbcorr':dopbcorr, 
                                   'conjbeams':conjbeams, 'computepastep':computepastep,
                                   'rotatepastep':rotatepastep, #'mtype':mtype, # 'weightlimit':weightlimit,
                                   'facets':facets, 'interpolation':interpolation, 'wprojplanes':wprojplanes,
                                   'deconvolver':deconvolver }     }
        ######### weighting
        self.weightpars = {'type':weighting,'robust':robust, 'npixels':npixels,'uvtaper':uvtaper}

        ######### Normalizers ( this is where flat noise, flat sky rules will go... )
        self.allnormpars = { self.defaultKey : {#'mtype': mtype,
                                 'pblimit': pblimit,'ntaylorterms':ntaylorterms,'facets':facets,
                                 'normtype':normtype, 'workdir':workdir,
                                 'deconvolver':deconvolver}     }

        ######### Deconvolution
        self.alldecpars = { self.defaultKey: { 'id':0, 'deconvolver':deconvolver, 'ntaylorterms':ntaylorterms, 
                                    'scales':scales, 'restoringbeam':restoringbeam, 'mask':mask,
                                    'interactive':interactive, 'startmodel':startmodel} }

        ######### Iteration control. 
        self.iterpars = { 'niter':niter, 'cycleniter':cycleniter, 'threshold':threshold, 
                          'loopgain':loopgain, 'interactive':interactive,
                          'cyclefactor':cyclefactor, 'minpsffraction':minpsffraction, 'maxpsffraction':maxpsffraction}

        ######### CFCache params. 
        self.cfcachepars = {'cflist': cflist};


        #self.reusename=reuse

        ## List of supported parameters in outlier files.
        ## All other parameters will default to the global values.
        self.outimparlist = ['imagename','nchan','imsize','cell','phasecenter','startmodel',
                             'start','width',
                             'ntaylorterms','reffreq','specmode']
        self.outgridparlist = ['gridder','deconvolver','wprojplanes']
        self.outweightparlist=[]
        self.outdecparlist=['deconvolver','startmodel','ntaylorterms','mask']
        self.outnormparlist=['deconvolver','weightlimit','ntaylorterms']
#        self.outnormparlist=['imagename','mtype','weightlimit','ntaylorterms']

        ret = self.checkParameters()
        if ret==False:
            casalog.post('Found errors in input parameters. Please check.', 'WARN')

        self.printParameters()

    def getSelPars(self):
        return self.allselpars
    def getImagePars(self):
        return self.allimpars
    def getGridPars(self):
        return self.allgridpars
    def getWeightPars(self):
        return self.weightpars
    def getDecPars(self):
        return self.alldecpars
    def getIterPars(self):
        return self.iterpars
    def getNormPars(self):
        return self.allnormpars
    def getCFCachePars(self):
        return self.cfcachepars;

    def setSelPars(self,selpars):
        self.allselpars = selpars
    def setImagePars(self,impars):
        self.allimpars = impars
    def setGridPars(self,gridpars):
        self.allgridpars = gridpars
    def setWeightPars(self,weightpars):
        self.weightpars = weightpars
    def setDecPars(self,decpars):
        self.alldecpars = decpars
    def setIterPars(self,iterpars):
        self.iterpars = iterpars
    def setNormPars(self,normpars):
        self.allnormpars = normpars



    def checkParameters(self):
        #casalog.origin('refimagerhelper.checkParameters')
        casalog.post('Verifying Input Parameters')
        # Init the error-string
        errs = "" 
        errs += self.checkAndFixSelectionPars()
        errs += self.makeImagingParamLists()
        errs += self.checkAndFixIterationPars()
        errs += self.checkAndFixNormPars()

        ### Copy them from 'impars' to 'normpars' and 'decpars'
        self.iterpars['allimages']={}
        for immod in self.allimpars.keys() :
            self.allnormpars[immod]['imagename'] = self.allimpars[immod]['imagename']
            self.alldecpars[immod]['imagename'] = self.allimpars[immod]['imagename']
            self.iterpars['allimages'][immod] = { 'imagename':self.allimpars[immod]['imagename'] , 'multiterm': (self.alldecpars[immod]['deconvolver']=='mtmfs') }

        ## If there are errors, print a message and exit.
        if len(errs) > 0:
#            casalog.post('Parameter Errors : \n' + errs,'WARN')
            raise Exception("Parameter Errors : \n" + errs)
 #           return False
        return True

    ###### Start : Parameter-checking functions ##################


    def checkAndFixSelectionPars(self):
        errs=""
        # msname, field, spw, etc must all be equal-length lists of strings, or all except msname must be of length 1.
        if not self.allselpars.has_key('msname'):
            errs = errs + 'MS name(s) not specified'
        else:

            selkeys = self.allselpars.keys()

            # Convert all non-list parameters into lists.
            for par in selkeys:
                if type( self.allselpars[par] ) != list:
                    self.allselpars[par] = [ self.allselpars[par]  ]
                    
            # Check that all are the same length as nvis
            # If not, and if they're single, replicate them nvis times
            nvis = len(self.allselpars['msname'])
            for par in selkeys:
                if len( self.allselpars[par] ) > 1 and len( self.allselpars[par] ) != nvis:
                    errs = errs + str(par) + ' must have a single entry, or ' + str(nvis) + ' entries to match vis list \n'
                    return errs
                else: # Replicate them nvis times if needed.
                    if len( self.allselpars[par] ) == 1:
                        for ms in range(1,nvis):
                            self.allselpars[par].append( self.allselpars[par][0] )
                    

            # Now, all parameters are lists of strings each of length 'nvis'.
            # Put them into separate dicts per MS.
            selparlist={}
            for ms in range(0,nvis):
                selparlist[ 'ms'+str(ms) ] = {}
                for par in selkeys:
                    selparlist[ 'ms'+str(ms) ][ par ] = self.allselpars[par][ms]

                synu = casac.synthesisutils()
                selparlist[ 'ms'+str(ms) ] = synu.checkselectionparams( selparlist[ 'ms'+str(ms)] )
                synu.done()

#            print selparlist

            self.allselpars = selparlist

        return errs


    def makeImagingParamLists(self ):
        errs=""

        ## Multiple images have been specified. 
        ## (1) Parse the outlier file and fill a list of imagedefinitions
        ## OR (2) Parse lists per input parameter into a list of parameter-sets (imagedefinitions)
        ### The code below implements (1)
        outlierpars=[]
        parseerrors=""
        if len(self.outlierfile)>0:
            outlierpars,parseerrors = self.parseOutlierFile(self.outlierfile) 

        if len(parseerrors)>0:
            errs = errs + "Errors in parsing outlier file : " + parseerrors
            return errs

        # Initialize outlier parameters with defaults
        # Update outlier parameters with modifications from outlier files
        for immod in range(0, len(outlierpars)):
            modelid = str(immod+1)
            self.allimpars[ modelid ] = copy.deepcopy(self.allimpars[ '0' ])
            self.allimpars[ modelid ].update(outlierpars[immod]['impars'])
            self.allgridpars[ modelid ] = copy.deepcopy(self.allgridpars[ '0' ])
            self.allgridpars[ modelid ].update(outlierpars[immod]['gridpars'])
            self.alldecpars[ modelid ] = copy.deepcopy(self.alldecpars[ '0' ])
            self.alldecpars[ modelid ].update(outlierpars[immod]['decpars'])
            self.allnormpars[ modelid ] = copy.deepcopy(self.allnormpars[ '0' ])
            self.allnormpars[ modelid ].update(outlierpars[immod]['normpars'])
            self.alldecpars[ modelid ][ 'id' ] = immod+1  ## Try to eliminate.


        #print self.allimpars

        for immod in self.allimpars.keys() :
            synu = casac.synthesisutils()
            self.allimpars[immod] = synu.checkimageparams( self.allimpars[immod] )
            synu.done()

        ## Check for name increments, and copy from impars to decpars and normpars.
        self.handleImageNames()

        return errs

    def handleImageNames(self):

            for immod in self.allimpars.keys() :
                inpname = self.allimpars[immod]['imagename']

                ### If a directory name is embedded in the image name, check that the dir exists.
                if inpname.count('/'):
                    splitname = inpname.split('/')
                    prefix = splitname[ len(splitname)-1 ]
                    dirname = './' + inpname[0: len(inpname)-len(prefix)]   # has '/' at end
                    if not os.path.exists( dirname ):
                        casalog.post('Making directory : ' + dirname, 'INFO')
                        os.mkdir( dirname )
                    
            ### Check for name increments 
            #if self.reusename == False:

            #### MPIInterface related changes
#            if self.allimpars['0']['overwrite'] == False:   # Later, can change this to be field dependent too.
            if self.allimpars['0']['overwrite'] == False:   # Later, can change this to be field dependent too.
                ## Get a list of image names for all fields (to sync name increment ids across fields)
                inpnamelist={}
                for immod in self.allimpars.keys() :
                    inpnamelist[immod] = self.allimpars[immod]['imagename'] 

                newnamelist = self.incrementImageNameList( inpnamelist )

                if len(newnamelist) != len(self.allimpars.keys()) :
                    casalog.post('Internal Error : Non matching list lengths in refimagerhelper::handleImageNames. Not updating image names','WARN')
                else : 
                    for immod in self.allimpars.keys() :
                        self.allimpars[immod]['imagename'] = newnamelist[immod]
                
#                newname = self.incrementImageName( inpname )
#                self.allimpars[immod]['imagename'] = newname

    def checkAndFixIterationPars(self ):
        errs=""

        # Bother checking only if deconvolution iterations are requested
        if self.iterpars['niter']>0:
            # Make sure cycleniter is less than or equal to niter. 
            if self.iterpars['cycleniter']<=0 or self.iterpars['cycleniter'] > self.iterpars['niter']:
                self.iterpars['cycleniter'] = self.iterpars['niter']

        return errs

    def checkAndFixNormPars(self):  
        errs=""

#        for modelid in self.allnormpars.keys():
#            if len(self.allnormpars[modelid]['workdir'])==0:
#                self.allnormpars[modelid]['workdir'] = self.allnormpars['0']['imagename'] + '.workdir'

        return errs

    ###### End : Parameter-checking functions ##################

    ## Parse outlier file and construct a list of imagedefinitions (dictionaries).
    def parseOutlierFile(self, outlierfilename="" ):
        returnlist = []
        errs=""  #  must be empty for no error

        if len(outlierfilename)>0 and not os.path.exists( outlierfilename ):
             errs +=  'Cannot find outlier file : ' +  outlierfilename + '\n'
             return returnlist, errs

        fp = open( outlierfilename, 'r' )
        thelines = fp.readlines()
        tempimpar={}
        tempgridpar={}
        tempweightpar={}
        tempdecpar={}
        tempnormpar={}
        for oneline in thelines:
            aline = oneline.replace('\n','')
#            aline = oneline.replace(' ','').replace('\n','')
            if len(aline)>0 and aline.find('#')!=0:
                parpair = aline.split("=")  
                parpair[0] = parpair[0].replace(' ','')
                #print parpair
                if len(parpair) != 2:
                    errs += 'Error in line containing : ' + oneline + '\n'
                if parpair[0] == 'imagename' and tempimpar != {}:
                    returnlist.append({'impars':tempimpar, 'gridpars':tempgridpar, 'weightpars':tempweightpar, 'decpars':tempdecpar} )
                    tempimpar={}
                    tempgridpar={}
                    tempweightpar={}
                    tempdecpar={}
                    tempnormpar={}
                usepar=False
                if parpair[0] in self.outimparlist:
                    tempimpar[ parpair[0] ] = parpair[1]
                    usepar=True
                if parpair[0] in self.outgridparlist:
                    tempgridpar[ parpair[0] ] = parpair[1]
                    usepar=True
                if parpair[0] in self.outweightparlist:
                    tempweightpar[ parpair[0] ] = parpair[1]
                    usepar=True
                if parpair[0] in self.outdecparlist:
                    tempdecpar[ parpair[0] ] = parpair[1]
                    usepar=True
                if parpair[0] in self.outnormparlist:
                    tempnormpar[ parpair[0] ] = parpair[1]
                    usepar=True
                if usepar==False:
                    print 'Ignoring unknown parameter pair : ' + oneline

        if len(errs)==0:
            returnlist.append( {'impars':tempimpar,'gridpars':tempgridpar, 'weightpars':tempweightpar, 'decpars':tempdecpar, 'normpars':tempnormpar} )

        ## Extra parsing for a few parameters.
        returnlist = self.evalToTarget( returnlist, 'impars', 'imsize', 'intvec' )
        returnlist = self.evalToTarget( returnlist, 'impars', 'nchan', 'int' )
        returnlist = self.evalToTarget( returnlist, 'impars', 'cell', 'strvec' )
        returnlist = self.evalToTarget( returnlist, 'impars', 'ntaylorterms', 'int' )
        returnlist = self.evalToTarget( returnlist, 'decpars', 'ntaylorterms', 'int' )
        returnlist = self.evalToTarget( returnlist, 'normpars', 'ntaylorterms', 'int' )
        returnlist = self.evalToTarget( returnlist, 'gridpars', 'wprojplanes', 'int' )
#        returnlist = self.evalToTarget( returnlist, 'impars', 'reffreq', 'strvec' )

        ## Extra parsing for a few parameters.
        ## imsize
#        try:
#            for fld in range(0, len( returnlist ) ):
#                if returnlist[ fld ]['impars'].has_key('imsize'):
#                    imsize_e = eval( returnlist[ fld ]['impars']['imsize'] )
#                    returnlist[ fld ]['impars']['imsize'] = imsize_e
#        except:
#            print 'Cannot evaluate outlier field parameter "imsize"'
#        ## nchan
#        try:
#            for fld in range(0, len( returnlist ) ):
#                if returnlist[ fld ]['impars'].has_key('nchan'):
#                    nchan_e = eval( returnlist[ fld ]['impars']['nchan'] )
#                    returnlist[ fld ]['impars']['nchan'] = nchan_e
#        except:
#            print 'Cannot evaluate outlier field parameter "nchan"'
#        ## cell
#        try:
#            for fld in range(0, len( returnlist ) ):
#                if returnlist[ fld ]['impars'].has_key('cell'):
#                    tcell =  returnlist[ fld ]['impars']['cell']
#                    tcell = tcell.replace(' ','').replace('[','').replace(']','').replace("'","")
#                    tcells = tcell.split(',')
#                    cell_e = []
#                    for cell in tcells:
#                        cell_e.append( cell )
#                    returnlist[ fld ]['impars']['cell'] = cell_e
#        except:
#            print 'Cannot evaluate outlier field parameter "cell"'
#        ## ntaylorterms (like nchan)
#        try:
#            for fld in range(0, len( returnlist ) ):
#                if returnlist[ fld ]['impars'].has_key('ntaylorterms'):
#                    nterms_e = eval( returnlist[ fld ]['impars']['ntaylorterms'] )
#                    returnlist[ fld ]['impars']['ntaylorterms'] = nterms_e
#        except:
#            print 'Cannot evaluate outlier field parameter "ntaylorterms"'
#        ## restfreq (like cell)
#        try:
#            for fld in range(0, len( returnlist ) ):
#                if returnlist[ fld ]['impars'].has_key('restfreq'):
#                    tcell =  returnlist[ fld ]['impars']['restfreq']
#                    tcell = tcell.replace(' ','').replace('[','').replace(']','').replace("'","")
#                    tcells = tcell.split(',')
#                    restfreq_e = []
#                    for cell in tcells:
#                        restfreq_e.append( cell )
#                    returnlist[ fld ]['impars']['restfreq'] = restfreq_e
#        except:
#            print 'Cannot evaluate outlier field parameter "restfreq"'
#
        #print returnlist
        return returnlist, errs


    def evalToTarget(self, globalpars, subparkey, parname, dtype='int' ):
        try:
            for fld in range(0, len( globalpars ) ):
                if globalpars[ fld ][subparkey].has_key(parname):
                    if dtype=='int' or dtype=='intvec':
                        val_e = eval( globalpars[ fld ][subparkey][parname] )
                    if dtype=='strvec':
                        tcell =  globalpars[ fld ][subparkey][parname]
                        tcell = tcell.replace(' ','').replace('[','').replace(']','').replace("'","")
                        tcells = tcell.split(',')
                        val_e = []
                        for cell in tcells:
                            val_e.append( cell )

                    globalpars[ fld ][subparkey][parname] = val_e
        except:
            print 'Cannot evaluate outlier field parameter "' + parname + '"'

        return globalpars


    def printParameters(self):
        casalog.post('SelPars : ' + str(self.allselpars), 'INFO2')
        casalog.post('ImagePars : ' + str(self.allimpars), 'INFO2')
        casalog.post('GridPars : ' + str(self.allgridpars), 'INFO2')
        casalog.post('NormPars : ' + str(self.allnormpars), 'INFO2')
        casalog.post('Weightpars : ' + str(self.weightpars), 'INFO2')
        casalog.post('DecPars : ' + str(self.alldecpars), 'INFO2')
        casalog.post('IterPars : ' + str(self.iterpars), 'INFO2')


    def incrementImageName(self,imagename):
        dirname = '.'
        prefix = imagename

        if imagename.count('/'):
            splitname = imagename.split('/')
            prefix = splitname[ len(splitname)-1 ]
            dirname = './' + imagename[0: len(imagename)-len(prefix)]   # has '/' at end

        inamelist = [fn for fn in os.listdir(dirname) if any([fn.startswith(prefix)])];

        if len(inamelist)==0:
            newimagename = dirname[2:] + prefix
        else:
            nlen = len(prefix)
            maxid=1
            for iname in inamelist:
                startind = iname.find( prefix+'_' )
                if startind==0:
                    idstr = ( iname[nlen+1:len(iname)] ).split('.')[0]
                    if idstr.isdigit() :
                        val = eval(idstr)
                        if val > maxid : 
                            maxid = val
            newimagename = dirname[2:] + prefix + '_' + str(maxid+1)

        print 'Using : ',  newimagename
        return newimagename

    def incrementImageNameList(self, inpnamelist ):

        dirnames={}
        prefixes={}

        for immod in inpnamelist.keys() : 
            imagename = inpnamelist[immod]
            dirname = '.'
            prefix = imagename

            if imagename.count('/'):
                splitname = imagename.split('/')
                prefix = splitname[ len(splitname)-1 ]
                dirname = './' + imagename[0: len(imagename)-len(prefix)]   # has '/' at end

            dirnames[immod] = dirname
            prefixes[immod] = prefix


        maxid=0
        for immod in inpnamelist.keys() : 
            prefix = prefixes[immod]
            inamelist = [fn for fn in os.listdir(dirnames[immod]) if any([fn.startswith(prefix)])];
            nlen = len(prefix)

            if len(inamelist)==0 : 
                locmax=0
            else: 
                locmax=1

            for iname in inamelist:
                startind = iname.find( prefix+'_' )
                if startind==0:
                    idstr = ( iname[nlen+1:len(iname)] ).split('.')[0]
                    if idstr.isdigit() :
                        val = eval(idstr)
                        if val > locmax : 
                            locmax = val
                            
            if locmax > maxid:
                maxid = locmax

        
        newimagenamelist={}
        for immod in inpnamelist.keys() : 
            if maxid==0 : 
                newimagenamelist[immod] = inpnamelist[immod]
            else:
                newimagenamelist[immod] = dirnames[immod][2:] + prefixes[immod] + '_' + str(maxid+1) 

#        print 'Input : ',  inpnamelist
#        print 'Dirs : ', dirnames
#        print 'Pre : ', prefixes
#        print 'Max id : ', maxid
#        print 'Using : ',  newimagenamelist
        return newimagenamelist






