module calcsound_fort_old

CONTAINS
!****************************************************
       SUBROUTINE cape_1d(Tin, Pin, Rin, Nparcels, NA, CAPERout, CAPEPout, PARout, PAPout)
!---------------------------------------------
! based on "calcsound.f" by Kerry A. Emanuel,
! ftp://texmex.mit.edu/pub/emanuel/BOOK/
!---------------------------------------------

!
!   ***   This program accepts input from the sounding contained   ***
!   ***      in the file <<sounding>> and calculates various       ***
!   ***       properties of samples of air raised or lowered       ***
!   ***                   to different levels.                     ***
!   ***      Output is tabulated in the file <<calcsound.out>>     ***
!   ***                 and in NCAR graphics files                 ***

!--- input variables -----------------
!   Tin [K], Pin [Pa], Rin [kg/kg]
!-------------------------------------

!---- output variables  ! all vars in [J/kg] -----
!   PAP    : Positive Area from pseudo-adiabatic ascent
!   PAR    : Positive Area from reversible ascent
!   NAP    : Negative Area from pseudo-adiabatic ascent
!   NAR    : Negative Area from reversible ascent
!   CAPEP  : CAPE from pseudo-adiabatic ascent
!   CAPER  : CAPE from reversible ascent
!   DCAPE  : Downdraft Convective Available Potential Energy 

!---------------------------------------------------
        IMPLICIT NONE

!        PARAMETER (NA=60)
        integer                                  NA
!--- input ------
        double precision,dimension(NA)        :: Tin, Pin, Rin
!f2py intent(in)                                 Tin, Pin, Rin
        integer                               :: Nparcels
!f2py intent(in)                                 Nparcels
!--- output -----
        double precision,dimension(Nparcels)  :: PARout, PAPout, NARout, NAPout
!f2py intent(out)                                PARout, PAPout, NARout, NAPout
        double precision,dimension(Nparcels)  :: CAPERout, CAPEPout, DCAPEout
!f2py intent(out)                                CAPERout, CAPEPout, DCAPEout


        REAL T(NA), P(NA), R(NA)
        REAL TLR(NA,NA), TLP(NA,NA)
        REAL EV(NA), ES(NA), TVRDIF(NA,NA), TVPDIF(NA,NA)
        REAL TLVR(NA,NA), TLVP(NA,NA), LW(NA,NA), TVD(NA)
!        REAL CAPER(NA), CAPEP(NA), DCAPE(NA), PAR(NA)
!        REAL PAP(NA), NAR(NA), NAP(NA)
        REAL CAPER(Nparcels), CAPEP(Nparcels), DCAPE(Nparcels), PAR(Nparcels)
        REAL PAP(Nparcels), NAR(Nparcels), NAP(Nparcels)



        !OPEN(UNIT=11, FILE='sounding', STATUS='OLD')
        !OPEN(UNIT=12, FILE='calcsound.out', STATUS='NEW')

!--- for calc -------
        INTEGER   I, ICB, IMAX, INBP, INBR, J, K, N
        REAL      AH, AHG, ALV, ALV1, CHI, CPW, EG, EM, ENEW&
       &          ,PLCL, PM, RG, RG0, RGD0, RH, RS, S, SG, SL&
       &          ,SLOPE, SLP, SP, SPD, SPG, SUM, SUM2&
       &          ,TC, TG, TG0, TGD0, TVDIFM, TVM


!   ***   ASSIGN VALUES OF THERMODYNAMIC CONSTANTS     ***
!
        real,parameter               :: CPD=1005.7
        real,parameter               :: CPV=1870.0
        real,parameter               :: CL=4190.0
        real,parameter               :: CPVMCL=2320.0
        real,parameter               :: RV=461.5
        real,parameter               :: RD=287.04
        real,parameter               :: EPS=RD/RV
        real,parameter               :: ALV0=2.501E6

!-- convert double --> real ----
        !T   = real(Tin) - 273.15  ! K  --> deg.C
        !P   = real(Pin) * 0.01   ! Pa --> hPa
        !R   = real(Rin) * 1000.   ! kg/kg --> g/Kg

        T   = real(Tin)
        P   = real(Pin) * 0.01   ! Pa --> hPa
        R   = real(Rin) 

!-- Number of levels -----------
        N   = NA

!-------------------------------
        !print *, "T",T
        !print *, "P",P
        !print *, "R",R

        DO 20 I=1,N
         EV(I)=R(I)*P(I)/(EPS+R(I))
         ES(I)=6.112*EXP(17.67*(T(I)-273.15)/(243.5+T(I)-273.15))
   20   CONTINUE     
!
!  ! ***   Read in the sounding from the file <<sounding>>          ***
!
   !     READ(11,10)N
   !10        FORMAT(4X,I3,//)
   !     DO 20 I=1,N
   !      READ(11,15)P(I),T(I),R(I)
   !15         FORMAT(5X,F9.3,8X,F9.3,12X,F9.3)
   !      R(I)=R(I)*0.001
   !      EV(I)=R(I)*P(I)/(EPS+R(I))
   !      ES(I)=6.112*EXP(17.67*T(I)/(243.5+T(I)))
   !      T(I)=T(I)+273.15
   !20        CONTINUE
   !     CLOSE(UNIT=11,DISPOSE='SAVE')
!
!   ***  Begin outer loop, which cycles through parcel origin levels I ***
!  
!     --- (a) calc CAPE for all levels ----
!        DO 500 I=1,N
!     --- (b) calc CAPE for the lowest parcel ----
        DO 500 I=1,Nparcels


!
!   ***  Define various conserved parcel quantities: reversible   ***
!   ***        entropy, S, pseudo-adiabatic entropy, SP,          *** 
!   ***                   and enthalpy, AH                        ***
!
        RS=EPS*ES(I)/(P(I)-ES(I))
        ALV=ALV0-CPVMCL*(T(I)-273.15)
        EM=MAX(EV(I),1.0E-6) 
        S=(CPD+R(I)*CL)*LOG(T(I))-RD*LOG(P(I)-EV(I))+&
     &    ALV*R(I)/T(I)-R(I)*RV*LOG(EM/ES(I))
        SP=CPD*LOG(T(I))-RD*LOG(P(I)-EV(I))+&
     &    ALV*R(I)/T(I)-R(I)*RV*LOG(EM/ES(I))
        AH=(CPD+R(I)*CL)*T(I)+ALV*R(I)
!      
!   ***  Find the temperature and mixing ratio of the parcel at   ***
!   ***    level I saturated by a wet bulb process                ***
!
        SLOPE=CPD+ALV*ALV*RS/(RV*T(I)*T(I))
        TG=T(I)
        RG=RS  
        !DO 100 J=1,20 
        DO 100 J=1,20 
         ALV1=ALV0-CPVMCL*(TG-273.15)
         AHG=(CPD+CL*RG)*TG+ALV1*RG
         TG=TG+(AH-AHG)/SLOPE
         TC=TG-273.15
         ENEW=6.112*EXP(17.67*TC/(243.5+TC))
         RG=EPS*ENEW/(P(I)-ENEW)
  100        CONTINUE
!   
!   ***  Calculate conserved variable at top of downdraft   ***
!
        EG=RG*P(I)/(EPS+RG)
        SPD=CPD*LOG(TG)-RD*LOG(P(I)-EG)+&
     &    ALV1*RG/TG
        TVD(I)=TG*(1.+RG/EPS)/(1.+RG)-T(I)*(1.+R(I)/EPS)/&
     &    (1.+R(I))
        IF(P(I).LT.100.0)TVD(I)=0.0
        RGD0=RG
        TGD0=TG
!
!   ***   Find lifted condensation pressure     ***
!
        RH=R(I)/RS
        RH=MIN(RH,1.0)
        CHI=T(I)/(1669.0-122.0*RH-T(I))
        PLCL=1.0
        IF(RH.GT.0.0)THEN
         PLCL=P(I)*(RH**CHI)
        END IF
!
!   ***  Begin updraft loop   ***
!
        SUM=0.0
        RG0=R(I)
        TG0=T(I)
        DO 200 J=I,N
!*         print *,"AAAAAAAAA"
!
!   ***  Calculate estimates of the rates of change of the entropies  ***
!   ***           with temperature at constant pressure               ***
!  
         RS=EPS*ES(J)/(P(J)-ES(J))
         ALV=ALV0-CPVMCL*(T(J)-273.15)
         SL=(CPD+R(I)*CL+ALV*ALV*RS/(RV*T(J)*T(J)))/T(J)
         SLP=(CPD+RS*CL+ALV*ALV*RS/(RV*T(J)*T(J)))/T(J)
!   
!   ***  Calculate lifted parcel temperature below its LCL   ***
!
         IF(P(J).GE.PLCL)THEN
          TLR(I,J)=T(I)*(P(J)/P(I))**(RD/CPD)
          TLP(I,J)=TLR(I,J) 
          LW(I,J)=0.0
          TLVR(I,J)=TLR(I,J)*(1.+R(I)/EPS)/(1.+R(I))
          TLVP(I,J)=TLVR(I,J)
          TVRDIF(I,J)=TLVR(I,J)-T(J)*(1.+R(J)/EPS)/(1.+R(J))
          TVPDIF(I,J)=TVRDIF(I,J)
         ELSE
!
!   ***  Iteratively calculate lifted parcel temperature and mixing   ***
!   ***    ratios for both reversible and pseudo-adiabatic ascent     ***
!
!*         TG=T(J)
!*         RG=RS
!*         DO 150 K=1,20
!*          EM=RG*P(J)/(EPS+RG)
!*          ALV=ALV0-CPVMCL*(TG-273.15)
!*          SG=(CPD+R(I)*CL)*LOG(TG)-RD*LOG(P(J)-EM)+&
!*     &      ALV*RG/TG
!*          TG=TG+(S-SG)/SL  
!*          TC=TG-273.15
!*          ENEW=6.112*EXP(17.67*TC/(243.5+TC))
!*          RG=EPS*ENEW/(P(J)-ENEW)           
!*  150         CONTINUE
!*         TLR(I,J)=TG
!*         TLVR(I,J)=TG*(1.+RG/EPS)/(1.+R(I))
!*         LW(I,J)=R(I)-RG
!*         LW(I,J)=MAX(0.0,LW(I,J))
!*         TVRDIF(I,J)=TLVR(I,J)-T(J)*(1.+R(J)/EPS)/(1.+R(J))
!
!   ***   Now do pseudo-adiabatic ascent   ***
!
         TG=T(J)
         RG=RS
         DO 180 K=1,20 
          CPW=0.0
          IF(J.GT.1)THEN
           CPW=SUM+CL*0.5*(RG0+RG)*(LOG(TG)-LOG(TG0))
          END IF
          EM=RG*P(J)/(EPS+RG)
          ALV=ALV0-CPVMCL*(TG-273.15)
          SPG=CPD*LOG(TG)-RD*LOG(P(J)-EM)+CPW+&
     &      ALV*RG/TG
          TG=TG+(SP-SPG)/SLP  
          TC=TG-273.15
          ENEW=6.112*EXP(17.67*TC/(243.5+TC))
          RG=EPS*ENEW/(P(J)-ENEW)           
  180         CONTINUE
         TLP(I,J)=TG
         TLVP(I,J)=TG*(1.+RG/EPS)/(1.+RG)
         TVPDIF(I,J)=TLVP(I,J)-T(J)*(1.+R(J)/EPS)/(1.+R(J))
         RG0=RG
         TG0=TG
         SUM=CPW
         END IF
  200        CONTINUE
        IF(I.EQ.1)GOTO 500
!
!   ***  Begin downdraft loop   ***
!
        SUM2=0.0
        DO 300 J=I-1,1,-1
!
!   ***  Calculate estimate of the rate of change of entropy          ***
!   ***           with temperature at constant pressure               ***
!  
         RS=EPS*ES(J)/(P(J)-ES(J))
         ALV=ALV0-CPVMCL*(T(J)-273.15)
         SLP=(CPD+RS*CL+ALV*ALV*RS/(RV*T(J)*T(J)))/T(J)
         TG=T(J)
         RG=RS
!
!   ***  Do iteration to find downdraft temperature   ***
!
         DO 250 K=1,20
          CPW=SUM2+CL*0.5*(RGD0+RG)*(LOG(TG)-LOG(TGD0))
          EM=RG*P(J)/(EPS+RG)
          ALV=ALV0-CPVMCL*(TG-273.15)
          SPG=CPD*LOG(TG)-RD*LOG(P(J)-EM)+CPW+&
     &      ALV*RG/TG
          TG=TG+(SPD-SPG)/SLP  
          TC=TG-273.15
          ENEW=6.112*EXP(17.67*TC/(243.5+TC))
          RG=EPS*ENEW/(P(J)-ENEW)           
  250         CONTINUE
         SUM2=CPW
         TGD0=TG
         RGD0=RG
         TLP(I,J)=TG
         TLVP(I,J)=TG*(1.+RG/EPS)/(1.+RG)
         TVPDIF(I,J)=TLVP(I,J)-T(J)*(1.+R(J)/EPS)/(1.+R(J))
         IF(P(I).LT.100.0)TVPDIF(I,J)=0.0
         TVPDIF(I,J)=MIN(TVPDIF(I,J),0.0)
         TLR(I,J)=T(J)
         TLVR(I,J)=T(J)
         TVRDIF(I,J)=0.0
         LW(I,J)=0.0
  300        CONTINUE
  500   CONTINUE
!
!  ***  Begin loop to find CAPE, PA, and NA from reversible and ***
!  ***            pseudo-adiabatic ascent, and DCAPE            ***
!

        DO 800 I=1,Nparcels
         CAPER(I)=0.0
         CAPEP(I)=0.0
         DCAPE(I)=0.0
         PAP(I)=0.0
         PAR(I)=0.0
         NAP(I)=0.0
         NAR(I)=0.0
!
!   ***   Find lifted condensation pressure     ***
!
        RS=EPS*ES(I)/(P(I)-ES(I))
        RH=R(I)/RS
        RH=MIN(RH,1.0)
        CHI=T(I)/(1669.0-122.0*RH-T(I))
        PLCL=1.0
        IF(RH.GT.0.0)THEN
         PLCL=P(I)*(RH**CHI)
        END IF
!
!   ***  Find lifted condensation level and maximum level   ***
!   ***               of positive buoyancy                  ***
!
         ICB=N
         INBR=1
         INBP=1
         DO 550 J=N,I,-1
          IF(P(J).LT.PLCL)ICB=MIN(ICB,J)
          IF(TVRDIF(I,J).GT.0.0)INBR=MAX(INBR,J)
          IF(TVPDIF(I,J).GT.0.0)INBP=MAX(INBP,J)
  550         CONTINUE
          IMAX=MAX(INBR+1,I)
           DO 555 J=IMAX,N
            TVRDIF(I,J)=0.0
  555           CONTINUE
          IMAX=MAX(INBP+1,I)
           DO 565 J=IMAX,N
            TVPDIF(I,J)=0.0
  565           CONTINUE
!
!   ***  Do updraft loops        ***
!
!*         IF(INBR.GT.I)THEN
!*          DO 600 J=I+1,INBR
!*           TVM=0.5*(TVRDIF(I,J)+TVRDIF(I,J-1))
!*           PM=0.5*(P(J)+P(J-1))
!*           IF(TVM.LE.0.0)THEN
!*            NAR(I)=NAR(I)-RD*TVM*(P(J-1)-P(J))/PM
!*           ELSE
!*            PAR(I)=PAR(I)+RD*TVM*(P(J-1)-P(J))/PM
!*           END IF
!*  600          CONTINUE
!*          CAPER(I)=PAR(I)-NAR(I)
!*         END IF
         IF(INBP.GT.I)THEN
          DO 650 J=I+1,INBP
           TVM=0.5*(TVPDIF(I,J)+TVPDIF(I,J-1))
           PM=0.5*(P(J)+P(J-1))
           IF(TVM.LE.0.0)THEN
            NAP(I)=NAP(I)-RD*TVM*(P(J-1)-P(J))/PM
           ELSE
            PAP(I)=PAP(I)+RD*TVM*(P(J-1)-P(J))/PM
           END IF
  650          CONTINUE
          CAPEP(I)=PAP(I)-NAP(I)
         END IF
!!
!!  ***       Find DCAPE     ***
!!
!         IF(I.EQ.1)GOTO 800
!         DO 700 J=I-1,1,-1
!          TVDIFM=TVPDIF(I,J+1)
!          IF(I.EQ.(J+1))TVDIFM=TVD(I)
!          TVM=0.5*(TVPDIF(I,J)+TVDIFM)
!          PM=0.5*(P(J)+P(J+1))
!          IF(TVM.LT.0.0)THEN
!           DCAPE(I)=DCAPE(I)-RD*TVM*(P(J)-P(J+1))/PM
!          END IF
!  700         CONTINUE                  
  800        CONTINUE
!*!
!*!  ***  Write values of PA, NA, CAPE and DCAPE   ***
!*!
!*        WRITE(*,801)
!*  801   FORMAT(20X,'ALL AREAS IN UNITS OF J/kg',//)
!*        WRITE(*,802)
!*  802        FORMAT(1X,'Origin',6X,'Rev.',6X,'P.A.',6X,'Rev.',6X,'P.A.',&
!*     &   6X,'Rev.',6X,'P.A.')
!*        WRITE(*,804)
!*  804        FORMAT(1X,'p (mb)',6X,' PA ',6X,' PA ',6X,' NA ',6X,' NA ',&
!*     &   6X,'CAPE',6X,'CAPE',6X,'DCAPE')
!*        WRITE(*,806)
!*  806        FORMAT(1X,'------',6X,'----',6X,'----',6X,'----',6X,'----',&
!*     &   6X,'----',6X,'----',6X,'-----')
!*        DO 820 I=1,Nparcels
!*         WRITE(*,810)P(I),PAR(I),PAP(I),NAR(I),NAP(I),CAPER(I),&
!*     &     CAPEP(I),DCAPE(I)
!*  810         FORMAT(1X,F8.1,7(F10.1))
!*  820        CONTINUE
!!
!!   ***  Use NCAR graphics to contour arrays of parcel buoyancy   ***
!!   ***    (Delete these if NCAR graphics are not available)      ***
!!
!        CALL OPNGKS
!        CALL CONREC(TVRDIF,NA,N,N,0.0,0.0,0.0,0,0,0)
!        CALL FRAME
!        CALL CONREC(TVPDIF,NA,N,N,0.0,0.0,0.0,0,0,0)
!        CALL FRAME
!        CALL CLSGKS
!        STOP
!

!*     write(*,*) "BBBBBBBBBB"

     CAPERout  = dble(CAPER)
     CAPEPout  = dble(CAPEP)
     !DCAPEout  = dble(DCAPE)
     PAPout    = dble(PAP)
     PARout    = dble(PAR)
     NARout    = dble(NAR)
     NAPout    = dble(NAP)
     !print *,"AAA CAPERout=",CAPERout(1)
     !print *,"AAA CAPEPout=",CAPEPout(1)
     !print *,"AAA CAPE

END SUBROUTINE cape_1d
!********************************************************
END MODULE calcsound_fort_old
