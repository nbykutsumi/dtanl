MODULE chart_fsub

CONTAINS
!*********************************************************
SUBROUTINE chartcyclone2saone(a2c_org, a2x_corres, a2y_corres, miss, nx_org, ny_org, a2c_saone)
implicit none
!----------------------
integer                              nx_org, ny_org
!------------------------
! front : 1->warm   2->cold  3->occ
!------------------------
real,dimension(nx_org, ny_org)    :: a2c_org
!f2py intent(in)                     a2c_org
!
real,dimension(nx_org, ny_org)    :: a2x_corres, a2y_corres
!f2py intent(in)                     a2x_corres, a2y_corres
real                                 miss
!f2py intent(in)                     miss
!--- out ----------
real,dimension(360,180)           :: a2c_saone, a2count_saone
!f2py intent(out)                    a2c_saone, a2count_saone
!--- calc ---------
integer                              ix, iy
integer                              ix_corres, iy_corres
integer                              ix_saone,  iy_saone
integer                              iix_saone,  iiy_saone
integer                              idx, idy
integer                              maxflag
!--- parameter  ---------
integer,parameter                    :: len_org = 10
!--- initialize ---------
a2c_saone          = 0.0
a2count_saone      = 0.0
!------------------------
! convert resolution a2org -> a2saone
!------------------------
do iy = 1,ny_org
  do ix = 1,nx_org
    !--------------------------------
    ix_corres  = int(a2x_corres(ix,iy))
    iy_corres  = int(a2y_corres(ix,iy))
    if ((ix_corres.eq.miss).or.(iy_corres.eq.miss))then
      cycle
    end if
    !--------------------------------
    if (a2c_org(ix,iy) .eq. 1.0) then
      a2count_saone(ix_corres,iy_corres) = a2count_saone(ix_corres,iy_corres) + 1.0
    end if
  end do 
end do
!------------------------
!------------------------
do iy_saone = 1, 180
  do ix_saone = 1, 360
    if (a2count_saone(ix_saone, iy_saone) .gt.0.0)then
      !--------------------------
      maxflag  = 1
      !--------------------------
      do idy = -1,1
        do idx = -1,1
          !---------------------
          call ixy2iixy_saone(ix_saone + idx, iy_saone + idy, iix_saone, iiy_saone)
          !---------------------
          if (a2count_saone(iix_saone, iiy_saone) .gt. a2count_saone(ix_saone, iy_saone))then
            maxflag = 0
          end if
        end do
      end do
      if ( maxflag .eq. 1)then
        print *,ix_saone,iy_saone
        a2c_saone(ix_saone,iy_saone) = 1.0
      end if
    end if
  end do
end do
!------------------------
do iy_saone = 1, 180
  do ix_saone = 1, 360
    if (a2c_saone(ix_saone, iy_saone) .eq. 1.0)then
      !--------------------------
      do idy = -1,1
        do idx = -1,1
          !---------------------
          call ixy2iixy_saone(ix_saone + idx, iy_saone + idy, iix_saone, iiy_saone)
          !---------------------
          if (a2c_saone(iix_saone, iiy_saone) .gt. 0.0)then
            print *,"BBBB",iix_saone,iiy_saone
            if ((idx.ne.0).and.(idy.ne.0))then
              a2c_saone(iix_saone, iiy_saone) = 0.0
              print *,"AAAA",iix_saone, iiy_saone
            end if
          end if
        end do
      end do
    end if
  end do
end do
!-----------
return
END SUBROUTINE chartcyclone2saone
!*********************************************************
SUBROUTINE chartfront2saone_new(a2front_org, a2x_corres, a2y_corres, miss, nx_org, ny_org, a2front_saone)
implicit none
!----------------------
integer                              nx_org, ny_org
!------------------------
! front : 1->warm   2->cold  3->occ
!------------------------
real,dimension(nx_org, ny_org)    :: a2front_org
!f2py intent(in)                     a2front_org
!
real,dimension(nx_org, ny_org)    :: a2x_corres, a2y_corres
!f2py intent(in)                     a2x_corres, a2y_corres
real                                 miss
!f2py intent(in)                     miss
!--- out ----------
real,dimension(360,180)           :: a2front_saone
!f2py intent(out)                    a2front_saone
!--- calc ---------
integer                              ix, iy
integer                              ix_corres, iy_corres
integer                              ix_saone,  iy_saone
integer                              ixt, iyt, idx, idy
integer                              ixn,ixs,ixe,ixw
integer                              iyn,iys,iye,iyw
integer                              ixnw, ixne, ixsw, ixse
integer                              iynw, iyne, iysw, iyse
real                                 wcount, ecount, scount, ncount, occcount_8grids, occcount_9x9, statcount_9x9
real                                 wcount_3opp, ecount_3opp, scount_3opp, ncount_3opp
real                                 wcount_same, ecount_same, scount_same, ncount_same
real                                 nwarm, ncold, nocc
real                                 tv, cv, cv_opp
real                                 vw, ve, vs, vn
real                                 vnw, vne, vsw, vse
real,dimension(360,180)           :: a2warm_saone, a2cold_saone, a2occ_saone
real,dimension(360,180)           :: a2flag_saone
real,dimension(360,180)           :: a2front_saone_temp
!--- parameter  ---------
real,parameter                    :: th_count_same = 4.0

!--- initialize ---------
a2front_saone  = miss
a2warm_saone   = 0.0
a2cold_saone   = 0.0
a2occ_saone    = 0.0
a2flag_saone   = 0.0
!------------------------
! convert front resolution a2org -> a2saone
!------------------------
do iy = 1,ny_org
  do ix = 1,nx_org
    !--------------------------------
    ix_corres  = int(a2x_corres(ix,iy))
    iy_corres  = int(a2y_corres(ix,iy))
    if ((ix_corres.eq.miss).or.(iy_corres.eq.miss))then
      cycle
    end if
    !--------------------------------
    if (a2front_org(ix,iy) .eq. 1.0) then
      a2warm_saone(ix_corres,iy_corres) = a2warm_saone(ix_corres,iy_corres) + 1.0
      a2flag_saone(ix_corres,iy_corres) = 1.0
    else if (a2front_org(ix,iy) .eq. 2.0 )then
      a2cold_saone(ix_corres,iy_corres) = a2cold_saone(ix_corres,iy_corres) + 1.0
      a2flag_saone(ix_corres,iy_corres) = 1.0

    else if (a2front_org(ix,iy) .eq. 3.0 )then
      a2occ_saone(ix_corres,iy_corres)  = a2occ_saone(ix_corres,iy_corres)  + 1.0
      a2flag_saone(ix_corres,iy_corres) = 1.0
    end if
  end do 
end do
!------------------------
do iy_saone = 1, 180
  do ix_saone = 1, 360
    if (a2flag_saone(ix_saone,iy_saone) .eq. 1.0) then
      nwarm   = a2warm_saone(ix_saone,iy_saone)
      ncold   = a2cold_saone(ix_saone,iy_saone)
      nocc    = a2occ_saone(ix_saone,iy_saone)
      if (nocc .gt. 1)then
        a2front_saone(ix_saone,iy_saone) = 3.0
      else if ((nwarm .gt. ncold).and.(nwarm .gt. nocc))then
        a2front_saone(ix_saone,iy_saone) = 1.0
      else if ((ncold .gt. nocc).and.(ncold .gt. nwarm))then
        a2front_saone(ix_saone,iy_saone) = 2.0
      end if
    end if
  end do
end do
!-----------
!***************************************************
! stationary front 1st
!---------------------------------------------------
a2front_saone_temp = a2front_saone
do iy_saone = 1, 180
  do ix_saone = 1, 360
    cv    = a2front_saone(ix_saone,iy_saone)
    if ((cv .eq.1).or.(cv.eq.2))then
      !*********************************************
      ! opposite color
      !---------------------------------------------
      if (cv .eq. 1)then
        cv_opp = 2
      else if (cv .eq. 2)then
        cv_opp = 1
      end if
      !*********************************************
      ! stationary front
      !---------------------------------------------
      wcount = 0.0
      ecount = 0.0
      scount = 0.0
      ncount = 0.0
      wcount_same = 0.0
      ecount_same = 0.0
      scount_same = 0.0
      ncount_same = 0.0
      wcount_3opp = 0.0
      ecount_3opp = 0.0
      scount_3opp = 0.0
      ncount_3opp = 0.0

      occcount_9x9 = 0.0
      !----------------------------
      ! check stationary front: west-direction
      !----------------------------
      do idy = -1,1
        do idx = -3,-1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.eq.cv_opp)then
            wcount = wcount +1.0  
          else if (tv.eq.cv)then
            wcount_same = wcount_same + 1.0
          end if
        end do 
      end do          
      !----------------------------
      ! check stationary front: east-direction
      !----------------------------
      do idy = -1,1
        do idx = 1,3
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.eq.cv_opp)then
            ecount = ecount +1.0  
          else if (tv.eq.cv)then
            ecount_same = ecount_same + 1.0
          end if

        end do 
      end do          
      !----------------------------
      ! check stationary front: south-direction
      !----------------------------
      do idy = -3,-1
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.eq.cv_opp)then
            scount = scount +1.0  
          else if (tv.eq.cv)then
            scount_same = scount_same + 1.0
          end if
        end do 
      end do          
      !----------------------------
      ! check stationary front: north-direction
      !----------------------------
      do idy = 1,3
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.eq.cv_opp)then
            ncount = ncount +1.0  
          else if (tv.eq.cv)then
            ncount_same = ncount_same + 1.0
          end if
        end do 
      end do          
      !----------------------------
      ! check stationary front: surrounding 9x9 grids
      !----------------------------
      do idy = -4,4
        do idx = -4,4
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.eq.3)then
            occcount_9x9 = occcount_9x9 +1
          end if
        end do 
      end do          
      !----------------------------
      ! adjacent 3 grids
      !----------------------------
      ! North ----------
      idy = 1
      do idx = -1,1
        CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
        tv = a2front_saone(ixt,iyt)
        if (tv.eq.cv_opp)then
          ncount_3opp  = ncount_3opp +1
        end if
      end do 

      ! South -----------
      idy = -1
      do idx = -1,1
        CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
        tv = a2front_saone(ixt,iyt)
        if (tv.eq.cv_opp)then
          scount_3opp  = scount_3opp +1
        end if
      end do 

      ! West -----------
      idx = -1
      do idy = -1,1
        CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
        tv = a2front_saone(ixt,iyt)
        if (tv.eq.cv_opp)then
          wcount_3opp  = wcount_3opp +1
        end if
      end do 

      ! East -----------
      idx = 1
      do idy = -1,1
        CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
        tv = a2front_saone(ixt,iyt)
        if (tv.eq.cv_opp)then
          ecount_3opp  = ecount_3opp +1
        end if
      end do 
      !----------------------------
      if ((ncount_same .lt.th_count_same )&
         .and.(scount_same.lt.th_count_same)&
         .and.(wcount_same.lt.th_count_same)&
         .and.(ecount_same.lt.th_count_same)) then
        if ((occcount_9x9.eq.0).and.(wcount.gt.0).and.(ecount.gt.0))then
          if ((ncount_3opp.lt.3).and.(scount_3opp.lt.3))then
            a2front_saone_temp(ix_saone,iy_saone)  = 4.0
          end if
        end if
        if ((occcount_9x9.eq.0).and.(scount.gt.0).and.(ncount.gt.0))then
          if ((wcount_3opp.lt.3).and.(ecount_3opp.lt.3))then
            a2front_saone_temp(ix_saone,iy_saone)  = 4.0
          end if
        end if
      end if
      !----------------------------
    end if
  end do
end do
!-- filter stationary front: continued a2front_saone_temp ---
do iy_saone = 1, 180
  do ix_saone = 1, 360
    cv    = a2front_saone_temp(ix_saone,iy_saone)
    if (cv .eq.4)then
      !*********************************************
      ! stationary front
      !---------------------------------------------
      statcount_9x9 = 0.0
      !----------------------------
      ! check stationary front: surrounding 9x9 grids
      !----------------------------
      do idy = -4,4
        do idx = -4,4
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone_temp(ixt,iyt)
          if (tv.eq.4)then
            statcount_9x9 = statcount_9x9 +1
          end if
        end do 
      end do          
      !----------------------------
      if (statcount_9x9.le.2)then
        a2front_saone_temp(ix_saone, iy_saone) = a2front_saone(ix_saone, iy_saone)
      end if
      !----------------------------
    end if
  end do
end do
a2front_saone = a2front_saone_temp

!**************************************************
! 2nd check stationary front
!---------------------------------------
do iy_saone = 1, 180
  do ix_saone = 1, 360
    cv    = a2front_saone(ix_saone,iy_saone)
    !if ((cv.eq.1).or.(cv.eq.2).or.(cv.eq.4))then
    if ((cv.eq.1).or.(cv.eq.2))then
      !*********************************************
      ! opposite color
      !---------------------------------------------
      if (cv .eq. 1)then
        cv_opp = 2
      else if (cv .eq. 2)then
        cv_opp = 1
      end if
      !---------------------------------------------
      wcount = 0.0
      ecount = 0.0
      scount = 0.0
      ncount = 0.0
      wcount_same = 0.0
      ecount_same = 0.0
      scount_same = 0.0
      ncount_same = 0.0
      wcount_3opp = 0.0
      ecount_3opp = 0.0
      scount_3opp = 0.0
      ncount_3opp = 0.0

      occcount_9x9 = 0.0
      !----------------------------
      ! 2nd check stationary front: west-direction
      !----------------------------
      do idy = -1,1
        do idx = -3,-1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if ((cv.ne.4).and.(tv.eq.cv_opp))then
            wcount = wcount +1.0  
          else if (tv.eq.cv)then
            wcount_same = wcount_same + 1.0
          end if
        end do 
      end do          
      !----------------------------
      ! 2nd check stationary front: east-direction
      !----------------------------
      do idy = -1,1
        do idx = 1,3
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if ((cv.ne.4).and.(tv.eq.cv_opp))then
            ecount = ecount +1.0  
          else if (tv.eq.cv)then
            ecount_same = ecount_same + 1.0
          end if
        end do 
      end do          
      !----------------------------
      ! 2nd check stationary front: south-direction
      !----------------------------
      do idy = -3,-1
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if ((cv.ne.4).and.(tv.eq.cv_opp))then
            scount = scount +1.0  
          else if (tv.eq.cv)then
            scount_same = scount_same + 1.0
          end if
        end do 
      end do          
      !----------------------------
      ! 2nd check stationary front: north-direction
      !----------------------------
      do idy = 1,3
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if ((cv.ne.4).and.(tv.eq.cv_opp))then
            ncount = ncount +1.0  
          else if (tv.eq.cv)then
            ncount_same = ncount_same + 1.0
          end if
        end do 
      end do          
      !----------------------------
      ! check stationary front: surrounding 9x9 grids
      !----------------------------
      do idy = -4,4
        do idx = -4,4
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.eq.3)then
            occcount_9x9 = occcount_9x9 +1
          end if
        end do 
      end do          
      !----------------------------
      ! adjacent 3 grids
      !----------------------------
      ! North ----------
      idy = 1
      do idx = -1,1
        CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
        tv = a2front_saone(ixt,iyt)
        if (tv.eq.cv_opp)then
          ncount_3opp  = ncount_3opp +1
        end if
      end do 

      ! South -----------
      idy = -1
      do idx = -1,1
        CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
        tv = a2front_saone(ixt,iyt)
        if (tv.eq.cv_opp)then
          scount_3opp  = scount_3opp +1
        end if
      end do 

      ! West -----------
      idx = -1
      do idy = -1,1
        CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
        tv = a2front_saone(ixt,iyt)
        if (tv.eq.cv_opp)then
          wcount_3opp  = wcount_3opp +1
        end if
      end do 

      ! East -----------
      idx = 1
      do idy = -1,1
        CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
        tv = a2front_saone(ixt,iyt)
        if (tv.eq.cv_opp)then
          ecount_3opp  = ecount_3opp +1
        end if
      end do 
      !----------------------------
      ! 2nd check stationary front: all
      !----------------------------
      if ((ncount_same .lt.th_count_same )&
         .and.(scount_same.lt.th_count_same)&
         .and.(wcount_same.lt.th_count_same)&
         .and.(ecount_same.lt.th_count_same)) then
        if ((occcount_9x9.eq.0).and.(wcount.gt.0).and.(ecount.gt.0))then
          if ((ncount_3opp.lt.3).and.(scount_3opp.lt.3))then
            a2front_saone_temp(ix_saone,iy_saone)  = 4.0
          end if
        end if
        if ((occcount_9x9.eq.0).and.(scount.gt.0).and.(ncount.gt.0))then
          if ((wcount_3opp.lt.3).and.(ecount_3opp.lt.3))then
            a2front_saone_temp(ix_saone,iy_saone)  = 4.0
          end if
        end if
      end if
    end if
  end do
end do
!-- filter stationary front: continued a2front_saone_temp ---
do iy_saone = 1, 180
  do ix_saone = 1, 360
    cv    = a2front_saone_temp(ix_saone,iy_saone)
    if (cv .eq.4)then
      !*********************************************
      ! stationary front
      !---------------------------------------------
      statcount_9x9 = 0.0
      !----------------------------
      ! check stationary front: surrounding 9x9 grids
      !----------------------------
      do idy = -4,4
        do idx = -4,4
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone_temp(ixt,iyt)
          if (tv.eq.4)then
            statcount_9x9 = statcount_9x9 +1
          end if
        end do 
      end do          
      !----------------------------
      if (statcount_9x9.le.2)then
        a2front_saone_temp(ix_saone, iy_saone) = a2front_saone(ix_saone, iy_saone)
      end if
      !----------------------------
    end if
  end do
end do



a2front_saone = a2front_saone_temp
!**************************************************
! 3rd check stationary front
!---------------------------------------
do iy_saone = 1, 180
  do ix_saone = 1, 360
    cv    = a2front_saone(ix_saone,iy_saone)
    if ((cv.eq.1).or.(cv.eq.2).or.(cv.eq.4))then
      wcount = 0.0
      ecount = 0.0
      scount = 0.0
      ncount = 0.0
      wcount_same = 0.0
      ecount_same = 0.0
      scount_same = 0.0
      ncount_same = 0.0
      occcount_9x9 = 0.0
      !----------------------------
      ! 3rd check stationary front: west-direction
      !----------------------------
      do idy = -1,1
        do idx = -3,-1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              wcount = wcount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              wcount_same = wcount_same + 1.0
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 3rd check stationary front: east-direction
      !----------------------------
      do idy = -1,1
        do idx = 1,3
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              ecount = ecount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              ecount_same = ecount_same + 1.0
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 3rd check stationary front: south-direction
      !----------------------------
      do idy = -3,-1
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              scount = scount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              scount_same = scount_same + 1.0
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 3rd check stationary front: north-direction
      !----------------------------
      do idy = 1,3
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              ncount = ncount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              ncount_same = ncount_same + 1.0
            end if
          end if
        end do 
      end do 
      !----------------------------
      ! check stationary front: surrounding 9x9 grids
      !----------------------------
      do idy = -4,4
        do idx = -4,4
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.eq.3)then
            occcount_9x9 = occcount_9x9 +1
          end if
        end do 
      end do          

      !----------------------------
      ! 3rd check stationary front: all
      !----------------------------
      if ((ncount_same .lt.th_count_same )&
         .and.(scount_same.lt.th_count_same)&
         .and.(wcount_same.lt.th_count_same)&
         .and.(ecount_same.lt.th_count_same)) then
        if (occcount_9x9 .eq. 0)then
          if      ((wcount.gt.0).and.(ecount_same.le.2))then
            a2front_saone_temp(ix_saone,iy_saone)  = 4.0
          else if ((ecount.gt.0).and.(wcount_same.le.2))then
            a2front_saone_temp(ix_saone,iy_saone)  = 4.0
          else if ((scount.gt.0).and.(ncount_same.le.2))then
            a2front_saone_temp(ix_saone,iy_saone)  = 4.0
          else if ((ncount.gt.0).and.(scount_same.le.2))then
            a2front_saone_temp(ix_saone,iy_saone)  = 4.0
          end if
        end if
      end if
    end if
  end do
end do
a2front_saone = a2front_saone_temp

!**************************************************
! 4th check stationary front
!---------------------------------------
do iy_saone = 1, 180
  do ix_saone = 1, 360
    cv    = a2front_saone(ix_saone,iy_saone)
    if ((cv.eq.1).or.(cv.eq.2).or.(cv.eq.4))then
      wcount = 0.0
      ecount = 0.0
      scount = 0.0
      ncount = 0.0
      wcount_same = 0.0
      ecount_same = 0.0
      scount_same = 0.0
      ncount_same = 0.0
      occcount_9x9 = 0.0
      !----------------------------
      ! 4th check stationary front: west-direction
      !----------------------------
      do idy = -1,1
        do idx = -3,-1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              wcount = wcount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              wcount_same = wcount_same + 1.0
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 4th check stationary front: east-direction
      !----------------------------
      do idy = -1,1
        do idx = 1,3
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              ecount = ecount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              ecount_same = ecount_same + 1.0
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 4th check stationary front: south-direction
      !----------------------------
      do idy = -3,-1
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              scount = scount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              scount_same = scount_same + 1.0
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 4th check stationary front: north-direction
      !----------------------------
      do idy = 1,3
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              ncount = ncount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              ncount_same = ncount_same + 1.0
            end if
          end if
        end do 
      end do 
      !----------------------------
      ! 4th check stationary front: surrounding 9x9 grids
      !----------------------------
      do idy = -4,4
        do idx = -4,4
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.eq.3)then
            occcount_9x9 = occcount_9x9 +1
          end if
        end do 
      end do          

      !----------------------------
      ! 4th check stationary front: all
      !----------------------------
      if ((ncount_same .lt.th_count_same )&
         .and.(scount_same.lt.th_count_same)&
         .and.(wcount_same.lt.th_count_same)&
         .and.(ecount_same.lt.th_count_same)) then
        if (occcount_9x9 .eq. 0)then
          if      ((wcount.gt.0).and.(ecount_same.le.2))then
            a2front_saone_temp(ix_saone,iy_saone)  = 4.0
          else if ((ecount.gt.0).and.(wcount_same.le.2))then
            a2front_saone_temp(ix_saone,iy_saone)  = 4.0
          else if ((scount.gt.0).and.(ncount_same.le.2))then
            a2front_saone_temp(ix_saone,iy_saone)  = 4.0
          else if ((ncount.gt.0).and.(scount_same.le.2))then
            a2front_saone_temp(ix_saone,iy_saone)  = 4.0
          end if
        end if
      end if 
    end if
  end do
end do
a2front_saone = a2front_saone_temp
!**************************************************
! 5th check stationary front
!---------------------------------------
do iy_saone = 1, 180
  do ix_saone = 1, 360
    cv    = a2front_saone(ix_saone,iy_saone)
    if ((cv.eq.1).or.(cv.eq.2).or.(cv.eq.4))then
      wcount = 0.0
      ecount = 0.0
      scount = 0.0
      ncount = 0.0
      wcount_same = 0.0
      ecount_same = 0.0
      scount_same = 0.0
      ncount_same = 0.0
      occcount_9x9 = 0.0
      !----------------------------
      ! 5th check stationary front: west-direction
      !----------------------------
      do idy = -1,1
        do idx = -3,-1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              wcount = wcount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              wcount_same = wcount_same + 1.0
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 5th check stationary front: east-direction
      !----------------------------
      do idy = -1,1
        do idx = 1,3
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              ecount = ecount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              ecount_same = ecount_same + 1.0
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 5th check stationary front: south-direction
      !----------------------------
      do idy = -3,-1
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              scount = scount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              scount_same = scount_same + 1.0
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 5th check stationary front: north-direction
      !----------------------------
      do idy = 1,3
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              ncount = ncount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              ncount_same = ncount_same + 1.0
            end if
          end if
        end do 
      end do 
      !----------------------------
      ! 5th check stationary front: surrounding 9x9 grids
      !----------------------------
      do idy = -4,4
        do idx = -4,4
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.eq.3)then
            occcount_9x9 = occcount_9x9 +1
          end if
        end do 
      end do          

      !----------------------------
      ! 5th check stationary front: all
      !----------------------------
      if ((ncount_same .lt.th_count_same )&
         .and.(scount_same.lt.th_count_same)&
         .and.(wcount_same.lt.th_count_same)&
         .and.(ecount_same.lt.th_count_same)) then
        if (occcount_9x9 .eq. 0)then
          if      ((wcount.gt.0).and.(ecount_same.le.2))then
            a2front_saone_temp(ix_saone,iy_saone)  = 4.0
          else if ((ecount.gt.0).and.(wcount_same.le.2))then
            a2front_saone_temp(ix_saone,iy_saone)  = 4.0
          else if ((scount.gt.0).and.(ncount_same.le.2))then
            a2front_saone_temp(ix_saone,iy_saone)  = 4.0
          else if ((ncount.gt.0).and.(scount_same.le.2))then
            a2front_saone_temp(ix_saone,iy_saone)  = 4.0
          end if
        end if
      end if
    end if
  end do
end do
a2front_saone = a2front_saone_temp

!**************************************************
! 6th check stationary front
!---------------------------------------
do iy_saone = 1, 180
  do ix_saone = 1, 360
    cv    = a2front_saone(ix_saone,iy_saone)
    if ((cv.eq.1).or.(cv.eq.2).or.(cv.eq.4))then
      wcount = 0.0
      ecount = 0.0
      scount = 0.0
      ncount = 0.0
      wcount_same = 0.0
      ecount_same = 0.0
      scount_same = 0.0
      ncount_same = 0.0
      occcount_9x9 = 0.0
      !----------------------------
      ! 6th check stationary front: west-direction
      !----------------------------
      do idy = -1,1
        do idx = -3,-1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              wcount = wcount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              wcount_same = wcount_same + 1.0
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 6th check stationary front: east-direction
      !----------------------------
      do idy = -1,1
        do idx = 1,3
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              ecount = ecount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              ecount_same = ecount_same + 1.0
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 6th check stationary front: south-direction
      !----------------------------
      do idy = -3,-1
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              scount = scount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              scount_same = scount_same + 1.0
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 6th check stationary front: north-direction
      !----------------------------
      do idy = 1,3
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              ncount = ncount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              ncount_same = ncount_same + 1.0
            end if
          end if
        end do 
      end do 
      !----------------------------
      ! 6th check stationary front: surrounding 9x9 grids
      !----------------------------
      do idy = -4,4
        do idx = -4,4
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.eq.3)then
            occcount_9x9 = occcount_9x9 +1
          end if
        end do 
      end do          

      !----------------------------
      ! 6th check stationary front: all
      !----------------------------
      if ((ncount_same .lt.th_count_same )&
         .and.(scount_same.lt.th_count_same)&
         .and.(wcount_same.lt.th_count_same)&
         .and.(ecount_same.lt.th_count_same)) then
        if (occcount_9x9 .eq. 0)then
          if      ((wcount.gt.0).and.(ecount_same.le.2))then
            a2front_saone_temp(ix_saone,iy_saone)  = 4.0
          else if ((ecount.gt.0).and.(wcount_same.le.2))then
            a2front_saone_temp(ix_saone,iy_saone)  = 4.0
          else if ((scount.gt.0).and.(ncount_same.le.2))then
            a2front_saone_temp(ix_saone,iy_saone)  = 4.0
          else if ((ncount.gt.0).and.(scount_same.le.2))then
            a2front_saone_temp(ix_saone,iy_saone)  = 4.0
          end if
        end if
      end if
    end if
  end do
end do
a2front_saone = a2front_saone_temp



!**********************************************
! occluded front
!----------------------------------------------
a2front_saone_temp = a2front_saone
do iy_saone = 1, 180
  do ix_saone = 1, 360
    cv    = a2front_saone(ix_saone,iy_saone)
    if ((cv.eq.1).or.(cv.eq.2).or.(cv.eq.4))then
      !*********************************************
      occcount_8grids = 0
      call ixy2iixy_saone(ix_saone, iy_saone+1, ixn, iyn)
      call ixy2iixy_saone(ix_saone, iy_saone-1, ixs, iys)
      call ixy2iixy_saone(ix_saone-1, iy_saone, ixw, iyw)
      call ixy2iixy_saone(ix_saone+1, iy_saone, ixe, iye)

      call ixy2iixy_saone(ix_saone-1, iy_saone+1, ixnw, iynw)
      call ixy2iixy_saone(ix_saone+1, iy_saone+1, ixne, iyne)
      call ixy2iixy_saone(ix_saone-1, iy_saone-1, ixsw, iysw)
      call ixy2iixy_saone(ix_saone+1, iy_saone-1, ixse, iyse)

      vs = a2front_saone(ixs,iys)
      vn = a2front_saone(ixn,iyn)
      vw = a2front_saone(ixw,iyw)
      ve = a2front_saone(ixe,iye)

      vne = a2front_saone(ixne,iyne)
      vnw = a2front_saone(ixnw,iynw)
      vse = a2front_saone(ixse,iyse)
      vsw = a2front_saone(ixsw,iysw)

      if (vs.eq.3)then
        occcount_8grids = occcount_8grids + 1
      end if
      if (vn.eq.3)then
        occcount_8grids = occcount_8grids + 1
      end if
      if (vw.eq.3)then
        occcount_8grids = occcount_8grids + 1
      end if
      if (ve.eq.3)then
        occcount_8grids = occcount_8grids + 1
      end if

      if (vsw.eq.3)then
        occcount_8grids = occcount_8grids + 1
      end if
      if (vse.eq.3)then
        occcount_8grids = occcount_8grids + 1
      end if
      if (vnw.eq.3)then
        occcount_8grids = occcount_8grids + 1
      end if
      if (vne.eq.3)then
        occcount_8grids = occcount_8grids + 1
      end if

      !-----
      if (occcount_8grids .gt. 0)then
        a2front_saone_temp(ix_saone,iy_saone) = 3.0
      end if
    end if
  end do
end do
a2front_saone = a2front_saone_temp
!---------------------------------------------------------
return
END SUBROUTINE chartfront2saone_new
!*********************************************************





!*********************************************************
SUBROUTINE chartfront2saone(a2front_org, a2x_corres, a2y_corres, miss, nx_org, ny_org, a2front_saone)
implicit none
!----------------------
integer                              nx_org, ny_org
!------------------------
! front : 1->warm   2->cold  3->occ
!------------------------
real,dimension(nx_org, ny_org)    :: a2front_org
!f2py intent(in)                     a2front_org
!
real,dimension(nx_org, ny_org)    :: a2x_corres, a2y_corres
!f2py intent(in)                     a2x_corres, a2y_corres
real                                 miss
!f2py intent(in)                     miss
!--- out ----------
real,dimension(360,180)           :: a2front_saone
!f2py intent(out)                    a2front_saone
!--- calc ---------
integer                              ix, iy
integer                              ix_corres, iy_corres
integer                              ix_saone,  iy_saone
integer                              ixt, iyt, idx, idy
integer                              ixn,ixs,ixe,ixw
integer                              iyn,iys,iye,iyw
integer                              ixnw, ixne, ixsw, ixse
integer                              iynw, iyne, iysw, iyse
real                                 wcount, ecount, scount, ncount, occcount, occcount_8grids
real                                 wcount_same, ecount_same, scount_same, ncount_same
real                                 nwarm, ncold, nocc
real                                 tv, cv
real                                 vw, ve, vs, vn
real                                 vnw, vne, vsw, vse
real,dimension(360,180)           :: a2warm_saone, a2cold_saone, a2occ_saone
real,dimension(360,180)           :: a2flag_saone
real,dimension(360,180)           :: a2front_saone_temp
!--- initialize ---------
a2front_saone  = miss
a2warm_saone   = 0.0
a2cold_saone   = 0.0
a2occ_saone    = 0.0
a2flag_saone   = 0.0
!------------------------
! convert front resolution a2org -> a2saone
!------------------------
do iy = 1,ny_org
  do ix = 1,nx_org
    !--------------------------------
    ix_corres  = int(a2x_corres(ix,iy))
    iy_corres  = int(a2y_corres(ix,iy))
    if ((ix_corres.eq.miss).or.(iy_corres.eq.miss))then
      cycle
    end if
    !--------------------------------
    if (a2front_org(ix,iy) .eq. 1.0) then
      a2warm_saone(ix_corres,iy_corres) = a2warm_saone(ix_corres,iy_corres) + 1.0
      a2flag_saone(ix_corres,iy_corres) = 1.0
    else if (a2front_org(ix,iy) .eq. 2.0 )then
      a2cold_saone(ix_corres,iy_corres) = a2cold_saone(ix_corres,iy_corres) + 1.0
      a2flag_saone(ix_corres,iy_corres) = 1.0

    else if (a2front_org(ix,iy) .eq. 3.0 )then
      a2occ_saone(ix_corres,iy_corres)  = a2occ_saone(ix_corres,iy_corres)  + 1.0
      a2flag_saone(ix_corres,iy_corres) = 1.0
    end if
  end do 
end do
!------------------------
do iy_saone = 1, 180
  do ix_saone = 1, 360
    if (a2flag_saone(ix_saone,iy_saone) .eq. 1.0) then
      nwarm   = a2warm_saone(ix_saone,iy_saone)
      ncold   = a2cold_saone(ix_saone,iy_saone)
      nocc    = a2occ_saone(ix_saone,iy_saone)
      if (nocc .gt. 1)then
        a2front_saone(ix_saone,iy_saone) = 3.0
      else if ((nwarm .gt. ncold).and.(nwarm .gt. nocc))then
        a2front_saone(ix_saone,iy_saone) = 1.0
      else if ((ncold .gt. nocc).and.(ncold .gt. nwarm))then
        a2front_saone(ix_saone,iy_saone) = 2.0
      end if
    end if
  end do
end do
!-----------
!***************************************************
! stationary front 1st
!---------------------------------------------------
a2front_saone_temp = a2front_saone
do iy_saone = 1, 180
  do ix_saone = 1, 360
    cv    = a2front_saone(ix_saone,iy_saone)
    if ((cv .eq.1).or.(cv.eq.2))then
      !*********************************************
      ! stationary front
      !---------------------------------------------
      wcount = 0.0
      ecount = 0.0
      scount = 0.0
      ncount = 0.0
      occcount = 0.0
      !----------------------------
      ! check stationary front: west-direction
      !----------------------------
      do idy = -1,1
        do idx = -3,-1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.3)then
              occcount = occcount + 1
            else if (tv.ne.cv)then
              wcount = wcount +1.0  
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! check stationary front: east-direction
      !----------------------------
      do idy = -1,1
        do idx = 1,3
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.3)then
              occcount = occcount +1
            else if (tv.ne.cv)then
              ecount = ecount +1.0  
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! check stationary front: south-direction
      !----------------------------
      do idy = -3,-1
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.3)then
              occcount = occcount +1
            else if (tv.ne.cv)then
              scount = scount +1.0  
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! check stationary front: north-direction
      !----------------------------
      do idy = 1,3
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.3)then
              occcount = occcount +1
            else if (tv.ne.cv)then
              ncount = ncount +1.0  
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! check stationary front: all
      !----------------------------
      if ((occcount.eq.0).and.(wcount.gt.0).and.(ecount.gt.0))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      end if
      if ((occcount.eq.0).and.(scount.gt.0).and.(ncount.gt.0))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      end if
    end if
  end do
end do
a2front_saone = a2front_saone_temp
!**************************************************
! 2nd check stationary front
!---------------------------------------
do iy_saone = 1, 180
  do ix_saone = 1, 360
    cv    = a2front_saone(ix_saone,iy_saone)
    if ((cv.eq.1).or.(cv.eq.2).or.(cv.eq.4))then
      wcount = 0.0
      ecount = 0.0
      scount = 0.0
      ncount = 0.0
      occcount = 0.0
      !----------------------------
      ! 2nd check stationary front: west-direction
      !----------------------------
      do idy = -1,1
        do idx = -3,-1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.3)then
              occcount = occcount + 1
            else if ((cv.ne.4).and.(tv.ne.cv))then
              wcount = wcount +1.0  
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 2nd check stationary front: east-direction
      !----------------------------
      do idy = -1,1
        do idx = 1,3
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.3)then
              occcount = occcount +1
            else if ((cv.ne.4).and.(tv.ne.cv))then
              ecount = ecount +1.0  
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 2nd check stationary front: south-direction
      !----------------------------
      do idy = -3,-1
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.3)then
              occcount = occcount +1
            else if ((cv.ne.4).and.(tv.ne.cv))then
              scount = scount +1.0  
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 2nd check stationary front: north-direction
      !----------------------------
      do idy = 1,3
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.3)then
              occcount = occcount +1
            else if ((cv.ne.4).and.(tv.ne.cv))then
              ncount = ncount +1.0  
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 2nd check stationary front: all
      !----------------------------
      if ((occcount.eq.0).and.(wcount.gt.0).and.(ecount.gt.0))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      end if
      if ((occcount.eq.0).and.(scount.gt.0).and.(ncount.gt.0))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      end if
      !----------------------------
      ! find occluded front: all
      !----------------------------
      if ((occcount.gt.0).and.(a2front_saone_temp(ix_saone,iy_saone).eq.4))then
        a2front_saone_temp(ix_saone,iy_saone)  = 3.0
      end if
    end if
  end do
end do
a2front_saone = a2front_saone_temp
!**************************************************
! 3rd check stationary front
!---------------------------------------
do iy_saone = 1, 180
  do ix_saone = 1, 360
    cv    = a2front_saone(ix_saone,iy_saone)
    if ((cv.eq.1).or.(cv.eq.2).or.(cv.eq.4))then
      wcount = 0.0
      ecount = 0.0
      scount = 0.0
      ncount = 0.0
      wcount_same = 0.0
      ecount_same = 0.0
      scount_same = 0.0
      ncount_same = 0.0
      occcount = 0.0
      !----------------------------
      ! 3rd check stationary front: west-direction
      !----------------------------
      do idy = -1,1
        do idx = -3,-1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              wcount = wcount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              wcount_same = wcount_same + 1.0
            end if
            if (tv.eq.3)then
              occcount = occcount + 1
            endif
          end if
        end do 
      end do          
      !----------------------------
      ! 3rd check stationary front: east-direction
      !----------------------------
      do idy = -1,1
        do idx = 1,3
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              ecount = ecount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              ecount_same = ecount_same + 1.0
            end if
            if (tv.eq.3)then
              occcount = occcount + 1
            endif
          end if
        end do 
      end do          
      !----------------------------
      ! 3rd check stationary front: south-direction
      !----------------------------
      do idy = -3,-1
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              scount = scount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              scount_same = scount_same + 1.0
            end if
            if (tv.eq.3)then
              occcount = occcount + 1
            endif
          end if
        end do 
      end do          
      !----------------------------
      ! 3rd check stationary front: north-direction
      !----------------------------
      do idy = 1,3
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              ncount = ncount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              ncount_same = ncount_same + 1.0
            end if
            if (tv.eq.3)then
              occcount = occcount + 1
            endif
          end if
        end do 
      end do 
      !----------------------------
      ! 3rd check stationary front: all
      !----------------------------
      if ((wcount.gt.0).and.(ecount_same.le.3))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      else if ((ecount.gt.0).and.(wcount_same.le.3))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      else if ((scount.gt.0).and.(ncount_same.lt.3))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      else if ((ncount.gt.0).and.(scount_same.lt.3))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      end if
      !
      if ((occcount.gt.0).and.(a2front_saone_temp(ix_saone,iy_saone).eq.4))then
        a2front_saone_temp(ix_saone,iy_saone)=3.0
      endif
    end if
  end do
end do
a2front_saone = a2front_saone_temp
!**************************************************
! 4th check stationary front
!---------------------------------------
do iy_saone = 1, 180
  do ix_saone = 1, 360
    cv    = a2front_saone(ix_saone,iy_saone)
    if ((cv.eq.1).or.(cv.eq.2).or.(cv.eq.4))then
      wcount = 0.0
      ecount = 0.0
      scount = 0.0
      ncount = 0.0
      wcount_same = 0.0
      ecount_same = 0.0
      scount_same = 0.0
      ncount_same = 0.0
      occcount = 0.0
      !----------------------------
      ! 4th check stationary front: west-direction
      !----------------------------
      do idy = -1,1
        do idx = -3,-1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              wcount = wcount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              wcount_same = wcount_same + 1.0
            end if
            if (tv.eq.3)then
              occcount = occcount + 1
            endif
          end if
        end do 
      end do          
      !----------------------------
      ! 4th check stationary front: east-direction
      !----------------------------
      do idy = -1,1
        do idx = 1,3
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              ecount = ecount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              ecount_same = ecount_same + 1.0
            end if
            if (tv.eq.3)then
              occcount = occcount + 1
            endif
          end if
        end do 
      end do          
      !----------------------------
      ! 4th check stationary front: south-direction
      !----------------------------
      do idy = -3,-1
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              scount = scount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              scount_same = scount_same + 1.0
            end if
            if (tv.eq.3)then
              occcount = occcount + 1
            endif
          end if
        end do 
      end do          
      !----------------------------
      ! 4th check stationary front: north-direction
      !----------------------------
      do idy = 1,3
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              ncount = ncount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              ncount_same = ncount_same + 1.0
            end if
            if (tv.eq.3)then
              occcount = occcount + 1
            endif
          end if
        end do 
      end do          
      !----------------------------
      ! 4th check stationary front: all
      !----------------------------
      if ((wcount.gt.0).and.(ecount_same.le.3))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      else if ((ecount.gt.0).and.(wcount_same.le.3))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      else if ((scount.gt.0).and.(ncount_same.lt.3))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      else if ((ncount.gt.0).and.(scount_same.lt.3))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      end if
      !
      if ((occcount.gt.0).and.(a2front_saone_temp(ix_saone,iy_saone).eq.4))then
        a2front_saone_temp(ix_saone,iy_saone)=3.0
      endif
    end if
  end do
end do
a2front_saone = a2front_saone_temp
!-------------------------------------
!**************************************************
! 5th check stationary front
!---------------------------------------
do iy_saone = 1, 180
  do ix_saone = 1, 360
    cv    = a2front_saone(ix_saone,iy_saone)
    if ((cv.eq.1).or.(cv.eq.2).or.(cv.eq.4))then
      wcount = 0.0
      ecount = 0.0
      scount = 0.0
      ncount = 0.0
      wcount_same = 0.0
      ecount_same = 0.0
      scount_same = 0.0
      ncount_same = 0.0
      occcount = 0.0
      !----------------------------
      ! 5th check stationary front: west-direction
      !----------------------------
      do idy = -1,1
        do idx = -3,-1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              wcount = wcount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              wcount_same = wcount_same + 1.0
            end if
            if (tv.eq.3)then
              occcount = occcount + 1
            endif
          end if
        end do 
      end do          
      !----------------------------
      ! 5th check stationary front: east-direction
      !----------------------------
      do idy = -1,1
        do idx = 1,3
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              ecount = ecount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              ecount_same = ecount_same + 1.0
            end if
            if (tv.eq.3)then
              occcount = occcount + 1
            endif
          end if
        end do 
      end do          
      !----------------------------
      ! 5th check stationary front: south-direction
      !----------------------------
      do idy = -3,-1
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              scount = scount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              scount_same = scount_same + 1.0
            end if
            if (tv.eq.3)then
              occcount = occcount + 1
            endif
          end if
        end do 
      end do          
      !----------------------------
      ! 5th check stationary front: north-direction
      !----------------------------
      do idy = 1,3
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              ncount = ncount +1.0  
            else if ((cv.ne.4).and.(tv.eq.cv))then
              ncount_same = ncount_same + 1.0
            end if
            if (tv.eq.3)then
              occcount = occcount + 1
            endif
          end if
        end do 
      end do          
      !----------------------------
      ! 5th check stationary front: all
      !----------------------------
      if ((wcount.gt.0).and.(ecount_same.le.3))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      else if ((ecount.gt.0).and.(wcount_same.le.3))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      else if ((scount.gt.0).and.(ncount_same.lt.3))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      else if ((ncount.gt.0).and.(scount_same.lt.3))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      end if
      !
      if ((occcount.gt.0).and.(a2front_saone_temp(ix_saone,iy_saone).eq.4))then
        a2front_saone_temp(ix_saone,iy_saone)=3.0
      endif
    end if
  end do
end do
a2front_saone = a2front_saone_temp
!-------------------------------------
!**********************************************
! occluded front
!----------------------------------------------
a2front_saone_temp = a2front_saone
do iy_saone = 1, 180
  do ix_saone = 1, 360
    cv    = a2front_saone(ix_saone,iy_saone)
    if ((cv.eq.1).or.(cv.eq.2).or.(cv.eq.4))then
      !*********************************************
      occcount_8grids = 0
      call ixy2iixy_saone(ix_saone, iy_saone+1, ixn, iyn)
      call ixy2iixy_saone(ix_saone, iy_saone-1, ixs, iys)
      call ixy2iixy_saone(ix_saone-1, iy_saone, ixw, iyw)
      call ixy2iixy_saone(ix_saone+1, iy_saone, ixe, iye)

      call ixy2iixy_saone(ix_saone-1, iy_saone+1, ixnw, iynw)
      call ixy2iixy_saone(ix_saone+1, iy_saone+1, ixne, iyne)
      call ixy2iixy_saone(ix_saone-1, iy_saone-1, ixsw, iysw)
      call ixy2iixy_saone(ix_saone+1, iy_saone-1, ixse, iyse)

      vs = a2front_saone(ixs,iys)
      vn = a2front_saone(ixn,iyn)
      vw = a2front_saone(ixw,iyw)
      ve = a2front_saone(ixe,iye)

      vne = a2front_saone(ixne,iyne)
      vnw = a2front_saone(ixnw,iynw)
      vse = a2front_saone(ixse,iyse)
      vsw = a2front_saone(ixsw,iysw)

      if (vs.eq.3)then
        occcount_8grids = occcount_8grids + 1
      end if
      if (vn.eq.3)then
        occcount_8grids = occcount_8grids + 1
      end if
      if (vw.eq.3)then
        occcount_8grids = occcount_8grids + 1
      end if
      if (ve.eq.3)then
        occcount_8grids = occcount_8grids + 1
      end if

      if (vsw.eq.3)then
        occcount_8grids = occcount_8grids + 1
      end if
      if (vse.eq.3)then
        occcount_8grids = occcount_8grids + 1
      end if
      if (vnw.eq.3)then
        occcount_8grids = occcount_8grids + 1
      end if
      if (vne.eq.3)then
        occcount_8grids = occcount_8grids + 1
      end if

      !-----
      if (occcount_8grids .gt. 0)then
        a2front_saone_temp(ix_saone,iy_saone) = 3.0
      end if
    end if
  end do
end do
a2front_saone = a2front_saone_temp
!---------------------------------------------------------
return
END SUBROUTINE chartfront2saone
!*********************************************************


!*********************************************************
SUBROUTINE chartfront2saone_old(a2front_org, a2x_corres, a2y_corres, miss, nx_org, ny_org, a2front_saone)
implicit none
!----------------------
integer                              nx_org, ny_org
!------------------------
! front : 1->warm   2->cold  3->occ
!------------------------
real,dimension(nx_org, ny_org)    :: a2front_org
!f2py intent(in)                     a2front_org
!
real,dimension(nx_org, ny_org)    :: a2x_corres, a2y_corres
!f2py intent(in)                     a2x_corres, a2y_corres
real                                 miss
!f2py intent(in)                     miss
!--- out ----------
real,dimension(360,180)           :: a2front_saone
!f2py intent(out)                    a2front_saone
!--- calc ---------
integer                              ix, iy
integer                              ix_corres, iy_corres
integer                              ix_saone,  iy_saone
integer                              ixt, iyt, idx, idy
integer                              ixn,ixs,ixe,ixw
integer                              iyn,iys,iye,iyw
integer                              ixnw, ixne, ixsw, ixse
integer                              iynw, iyne, iysw, iyse
real                                 wcount, ecount, scount, ncount, occcount, occcount_8grids
real                                 wcount_same, ecount_same, scount_same, ncount_same
real                                 nwarm, ncold, nocc
real                                 tv, cv
real                                 vw, ve, vs, vn
real                                 vnw, vne, vsw, vse
real,dimension(360,180)           :: a2warm_saone, a2cold_saone, a2occ_saone
real,dimension(360,180)           :: a2flag_saone
real,dimension(360,180)           :: a2front_saone_temp
!--- initialize ---------
a2front_saone  = miss
a2warm_saone   = 0.0
a2cold_saone   = 0.0
a2occ_saone    = 0.0
a2flag_saone   = 0.0
!------------------------
! convert front resolution a2org -> a2saone
!------------------------
do iy = 1,ny_org
  do ix = 1,nx_org
    !--------------------------------
    ix_corres  = int(a2x_corres(ix,iy))
    iy_corres  = int(a2y_corres(ix,iy))
    if ((ix_corres.eq.miss).or.(iy_corres.eq.miss))then
      cycle
    end if
    !--------------------------------
    if (a2front_org(ix,iy) .eq. 1.0) then
      a2warm_saone(ix_corres,iy_corres) = a2warm_saone(ix_corres,iy_corres) + 1.0
      a2flag_saone(ix_corres,iy_corres) = 1.0
    else if (a2front_org(ix,iy) .eq. 2.0 )then
      a2cold_saone(ix_corres,iy_corres) = a2cold_saone(ix_corres,iy_corres) + 1.0
      a2flag_saone(ix_corres,iy_corres) = 1.0

    else if (a2front_org(ix,iy) .eq. 3.0 )then
      a2occ_saone(ix_corres,iy_corres)  = a2occ_saone(ix_corres,iy_corres)  + 1.0
      a2flag_saone(ix_corres,iy_corres) = 1.0
    end if
  end do 
end do
!------------------------
do iy_saone = 1, 180
  do ix_saone = 1, 360
    if (a2flag_saone(ix_saone,iy_saone) .eq. 1.0) then
      nwarm   = a2warm_saone(ix_saone,iy_saone)
      ncold   = a2cold_saone(ix_saone,iy_saone)
      nocc    = a2occ_saone(ix_saone,iy_saone)
      if (nocc .gt. 1)then
        a2front_saone(ix_saone,iy_saone) = 3.0
      else if ((nwarm .gt. ncold).and.(nwarm .gt. nocc))then
        a2front_saone(ix_saone,iy_saone) = 1.0
      else if ((ncold .gt. nocc).and.(ncold .gt. nwarm))then
        a2front_saone(ix_saone,iy_saone) = 2.0
      end if
    end if
  end do
end do
!-----------

a2front_saone_temp = a2front_saone
do iy_saone = 1, 180
  do ix_saone = 1, 360
    cv    = a2front_saone(ix_saone,iy_saone)
    if ((cv .gt. 0.0).and.(cv .ne. 3))then
      !*********************************************
      ! stationary front
      !---------------------------------------------
      wcount = 0.0
      ecount = 0.0
      scount = 0.0
      ncount = 0.0
      occcount = 0.0
      !----------------------------
      ! check stationary front: west-direction
      !----------------------------
      do idy = -1,1
        do idx = -3,-1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.3)then
              occcount = occcount + 1
            else if (tv.ne.cv)then
              wcount = wcount +1.0  
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! check stationary front: east-direction
      !----------------------------
      do idy = -1,1
        do idx = 1,3
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.3)then
              occcount = occcount +1
            else if (tv.ne.cv)then
              ecount = ecount +1.0  
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! check stationary front: south-direction
      !----------------------------
      do idy = -3,-1
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.3)then
              occcount = occcount +1
            else if (tv.ne.cv)then
              scount = scount +1.0  
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! check stationary front: north-direction
      !----------------------------
      do idy = 1,3
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.3)then
              occcount = occcount +1
            else if (tv.ne.cv)then
              ncount = ncount +1.0  
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! check stationary front: all
      !----------------------------
      if ((occcount.eq.0).and.(wcount.gt.0).and.(ecount.gt.0))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      end if
      if ((occcount.eq.0).and.(scount.gt.0).and.(ncount.gt.0))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      end if
      !*********************************************
      ! occluded front
      !---------------------------------------------
      if (occcount .gt. 0)then
        occcount_8grids = 0
        call ixy2iixy_saone(ix_saone, iy_saone+1, ixn, iyn)
        call ixy2iixy_saone(ix_saone, iy_saone-1, ixs, iys)
        call ixy2iixy_saone(ix_saone-1, iy_saone, ixw, iyw)
        call ixy2iixy_saone(ix_saone+1, iy_saone, ixe, iye)

        call ixy2iixy_saone(ix_saone-1, iy_saone+1, ixnw, iynw)
        call ixy2iixy_saone(ix_saone+1, iy_saone+1, ixne, iyne)
        call ixy2iixy_saone(ix_saone-1, iy_saone-1, ixsw, iysw)
        call ixy2iixy_saone(ix_saone+1, iy_saone-1, ixse, iyse)

        vs = a2front_saone(ixs,iys)
        vn = a2front_saone(ixn,iyn)
        vw = a2front_saone(ixw,iyw)
        ve = a2front_saone(ixe,iye)

        vne = a2front_saone(ixne,iyne)
        vnw = a2front_saone(ixnw,iynw)
        vse = a2front_saone(ixse,iyse)
        vsw = a2front_saone(ixsw,iysw)

        if (vs.eq.3)then
          occcount_8grids = occcount_8grids + 1
        end if
        if (vn.eq.3)then
          occcount_8grids = occcount_8grids + 1
        end if
        if (vw.eq.3)then
          occcount_8grids = occcount_8grids + 1
        end if
        if (ve.eq.3)then
          occcount_8grids = occcount_8grids + 1
        end if

        if (vsw.eq.3)then
          occcount_8grids = occcount_8grids + 1
        end if
        if (vse.eq.3)then
          occcount_8grids = occcount_8grids + 1
        end if
        if (vnw.eq.3)then
          occcount_8grids = occcount_8grids + 1
        end if
        if (vne.eq.3)then
          occcount_8grids = occcount_8grids + 1
        end if

        !-----
        if (occcount_8grids .gt. 0)then
          a2front_saone_temp(ix_saone,iy_saone) = 3.0
        end if
      end if
    end if
  end do
end do
a2front_saone = a2front_saone_temp
!**************************************************
! 2nd check stationary front
!---------------------------------------
do iy_saone = 1, 180
  do ix_saone = 1, 360
    cv    = a2front_saone(ix_saone,iy_saone)
    if ((cv.eq.1).or.(cv.eq.2))then
      wcount = 0.0
      ecount = 0.0
      scount = 0.0
      ncount = 0.0
      occcount = 0.0
      !----------------------------
      ! 2nd check stationary front: west-direction
      !----------------------------
      do idy = -1,1
        do idx = -3,-1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.3)then
              occcount = occcount + 1
            else if (tv.ne.cv)then
              wcount = wcount +1.0  
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 2nd check stationary front: east-direction
      !----------------------------
      do idy = -1,1
        do idx = 1,3
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.3)then
              occcount = occcount +1
            else if (tv.ne.cv)then
              ecount = ecount +1.0  
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 2nd check stationary front: south-direction
      !----------------------------
      do idy = -3,-1
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.3)then
              occcount = occcount +1
            else if (tv.ne.cv)then
              scount = scount +1.0  
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 2nd check stationary front: north-direction
      !----------------------------
      do idy = 1,3
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.3)then
              occcount = occcount +1
            else if (tv.ne.cv)then
              ncount = ncount +1.0  
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 2nd check stationary front: all
      !----------------------------
      if ((occcount.eq.0).and.(wcount.gt.0).and.(ecount.gt.0))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      end if
      if ((occcount.eq.0).and.(scount.gt.0).and.(ncount.gt.0))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      end if
    end if
  end do
end do
a2front_saone = a2front_saone_temp
!**************************************************
! 3rd check stationary front
!---------------------------------------
do iy_saone = 1, 180
  do ix_saone = 1, 360
    cv    = a2front_saone(ix_saone,iy_saone)
    if ((cv.eq.1).or.(cv.eq.2))then
      wcount = 0.0
      ecount = 0.0
      scount = 0.0
      ncount = 0.0
      wcount_same = 0.0
      ecount_same = 0.0
      scount_same = 0.0
      ncount_same = 0.0
      !----------------------------
      ! 3rd check stationary front: west-direction
      !----------------------------
      do idy = -1,1
        do idx = -3,-1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              wcount = wcount +1.0  
            else if (tv.eq.cv)then
              wcount_same = wcount_same + 1.0
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 3rd check stationary front: east-direction
      !----------------------------
      do idy = -1,1
        do idx = 1,3
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              ecount = ecount +1.0  
            else if (tv.eq.cv)then
              ecount_same = ecount_same + 1.0
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 3rd check stationary front: south-direction
      !----------------------------
      do idy = -3,-1
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              scount = scount +1.0  
            else if (tv.eq.cv)then
              scount_same = scount_same + 1.0
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 3rd check stationary front: north-direction
      !----------------------------
      do idy = 1,3
        do idx = -1,1
          CALL ixy2iixy_saone(ix_saone+idx, iy_saone+idy, ixt, iyt)
          tv = a2front_saone(ixt,iyt)
          if (tv.gt.0.0)then
            if (tv.eq.4)then
              ncount = ncount +1.0  
            else if (tv.eq.cv)then
              ncount_same = ncount_same + 1.0
            end if
          end if
        end do 
      end do          
      !----------------------------
      ! 3rd check stationary front: all
      !----------------------------
      if ((wcount.gt.0).and.(ecount_same.le.3))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      else if ((ecount.gt.0).and.(wcount_same.le.3))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      else if ((scount.gt.0).and.(ncount_same.lt.3))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      else if ((ncount.gt.0).and.(scount_same.lt.3))then
        a2front_saone_temp(ix_saone,iy_saone)  = 4.0
      end if
    end if
  end do
end do

a2front_saone = a2front_saone_temp

return
END SUBROUTINE chartfront2saone_old
!*********************************************************
SUBROUTINE ixy2iixy_saone(ix, iy, iix, iiy)
!--------------------------
! data array order should be "South->North" & "West->East"
! data array : nx= 360, ny= 180
!--------------------------
implicit none
!--- input -----------
integer             ix, iy
!f2py intent(in)    ix, iy
!--- output ----------
integer             iix, iiy
!f2py intent(out)   iix, iiy
!--- calc  -----------
!---------------------
if (iy .le. 0)then
  iiy = 1 - iy
  iix = ix + 180
else if (iy .ge. 181) then
  iiy = 2*180 - iy +1
  iix = ix + 180
else
  iiy = iy
  iix = ix
end if
!
if (iix .ge. 361) then
  iix = mod(iix, 360)
else if (iix .le. 0) then
  iix = 360 - mod(abs(iix), 360)
end if
!
return
END SUBROUTINE ixy2iixy_saone
!*********************************************************
!**************************************************************
FUNCTION hubeny_real(lat1, lon1, lat2, lon2)
  implicit none
  !-- for input -----------
  real                                  lat1, lon1, lat2, lon2
!f2py intent(in)                        lat1, lon1, lat2, lon2
  !-- for output-----------
  real                                  hubeny_real
!f2py intent(out)                       hubeny_real
  !-- for calc ------------
  real,parameter                     :: pi = atan(1.0)*4.0
  real,parameter                     :: a  = 6378137
  real,parameter                     :: b  = 6356752.314140
  real,parameter                     :: e2 = 0.00669438002301188
  real,parameter                     :: a_1_e2 = 6335439.32708317
  real                                  M, N, W
  real                                  latrad1, latrad2, lonrad1, lonrad2
  real                                  latave, dlat, dlon
  real                                  dlondeg
  !------------------------
  latrad1   = lat1 * pi / 180.0
  latrad2   = lat2 * pi / 180.0
  lonrad1   = lon1 * pi / 180.0
  lonrad2   = lon2 * pi / 180.0
  !
  latave    = (latrad1 + latrad2)/2.0
  dlat      = latrad2 - latrad1
  dlon      = lonrad2 - lonrad1
  !
  dlondeg   = lon2 - lon1
  if ( abs(dlondeg) .gt. 180.0) then
    dlondeg = 180.0 - mod(abs(dlondeg), 180.0)
    dlon    = dlondeg * pi / 180.0
  end if
  !-------
  W  = sqrt(1.0 - e2 * sin(latave)**2.0 )
  M  =  a_1_e2 / (W**3.0)
  N  =  a / W
  hubeny_real  = sqrt( (dlat * M)**2.0 + (dlon * N * cos(latave))**2.0 )
RETURN
END FUNCTION hubeny_real
!**************************************************************
!**************************************************************
SUBROUTINE mk_a2grad_saone(a2in, a2gradx, a2grady)
!---------------------------------
! data order should be South -> North, West -> East
! returns two vector map (map of da/dx, map of da/dy)
!---------------------------------
implicit none
!--- in ----------
integer                 :: ny = 180
integer                 :: nx = 360
real,dimension(360,180) :: a2in
!f2py intent(in)           a2in
!--- out ---------
real,dimension(360,180) :: a2gradx, a2grady
!f2py intent(out)          a2gradx, a2grady
!--- para --------
real                    :: lat_first = -89.5
!--- calc --------
real                       dn, ds, dew
real                       vn, vs, vw, ve
real                       lat
integer                    ix,  iy
integer                    ixn, ixs, ixw, ixe
integer                    iyn, iys, iyw, iye
!-----------------
do iy = 1, ny
  lat = lat_first + (iy -1)*1.0
  dn  = hubeny_real(lat, 0.0, lat+1.0, 0.0)
  ds  = hubeny_real(lat, 0.0, lat-1.0, 0.0)
  dew = hubeny_real(lat, 0.0, lat, 1.0)
  do ix = 1, nx
    !---
    call ixy2iixy_saone(ix, iy+1, ixn, iyn)
    call ixy2iixy_saone(ix, iy-1, ixs, iys)
    call ixy2iixy_saone(ix-1, iy, ixw, iyw)
    call ixy2iixy_saone(ix+1, iy, ixe, iye)
    !---
    vn = a2in(ixn, iyn)
    vs = a2in(ixs, iys)
    vw = a2in(ixw, iyw)
    ve = a2in(ixe, iye)
    !---
    a2gradx(ix, iy) = (ve - vw) / (2.0*dew)
    a2grady(ix, iy) = (vn - vs) / (dn + ds)

  end do
end do
!-----------------
return
END SUBROUTINE mk_a2grad_saone
!**************************************************************
!*********************************************************
END MODULE chart_fsub
