
    MODULE MainModule


    
    PROC goToCalibPos()
        VAR jointtarget calibPos := [[0.00341333,-129.995,30.0196,-0.000788279,40.0913,-0.461743],[134.997,9E+09,9E+09,9E+09,9E+09,9E+09]];
        MoveAbsJ calibPos\NoEOffs,v1000,z50,tool0;
    ENDPROC

    PROC Main()

        runall;
    ENDPROC

    PROC runall()
        FOR i FROM 1 TO DIM(nRadius, 1) DO
            runtest convergencePos{i}, nRadius{i};
        ENDFOR
    ENDPROC



    PROC MoveToDist(num dist,num h,\speeddata sp, PERS wobjdata wobjHeart)
        !   VAR robtarget position := [[0,0,0],[0.0,0.0,0.7071,-0.7071],[1,1,0,4],[143.284,9E+09,9E+09,9E+09,9E+09,9E+09]];
        VAR robtarget position:=[[0,0,0],[0.5,0.5,0.5,0.5],[1,-2,0,0],[-163.142,9E+09,9E+09,9E+09,9E+09,9E+09]];
        VAR num angle;
        VAR num halfdist;
        VAR num rads;
        VAR num zh;
        VAR num y;
        VAR speeddata speed;
        
        halfdist:=dist/2;
        speed:=speedSlow;
        angle:=ASin(halfdist/h);
        y:=h*sin(angle);
        zh:=h*cos(angle);

        position.trans:=[x,-y,zh];
        IF Present(sp) THEN
            speed:=sp;
        ENDIF
        MoveL RelTool(position,0,0,0\Ry:=y_offs\Rz:=angle+z_offs),speed,fine,tCamL\WObj:=wobjHeart;


    ENDPROC





    PROC gotoraisedpos()

        ReSet Collision_Avoidance;
        ConfL\Off;
        WaitSyncTask syncraise,tasklist;
        MoveAbsJ jtraised\NoEOffs,v100,fine,tCamL;

    ENDPROC

    PROC inc()
        goto1100;
    ENDPROC


    PROC incinc()
        goto1100;
    ENDPROC


    PROC dec()
        goto1100;
    ENDPROC


    PROC decdec()
        goto1100;
    ENDPROC



    PROC incX()
        goto1100;
    ENDPROC


    PROC incincX()

        goto1100;
    ENDPROC


    PROC decX()

        goto1100;

    ENDPROC


    PROC decdecX()
        goto1100;

    ENDPROC

    PROC gofrombatpos()
        VAR jointtarget jtVia := [[-68.4054,-105.589,37.6928,245.742,40.601,-189.436],[135.726,9E+09,9E+09,9E+09,9E+09,9E+09]];
        ReSet Collision_Avoidance;
        ConfL\Off;
        WaitSyncTask syncraise,tasklist;
        MoveAbsJ jtVia\NoEOffs,v100,fine,tCamL;
        MoveAbsJ jtraised\NoEOffs,v100,fine,tCamL;

    ENDPROC

    PROC gotobatpos()
        VAR jointtarget jtBatPos := [[-68.4054,-105.589,37.6928,245.742,40.601,-189.436],[135.726,9E+09,9E+09,9E+09,9E+09,9E+09]];
        ReSet Collision_Avoidance;
        ConfL\Off;
        MoveAbsJ jtraised\NoEOffs,v100,fine,tCamL;
        WaitSyncTask syncbat1,tasklist;
        MoveAbsJ jtBatPos\NoEOffs,v100,fine,tCamL;
        MoveAbsJ jtbat\NoEOffs,v100,fine,tCamL;
        WaitSyncTask syncbat2,tasklist;
    ENDPROC


    PROC gotoX1()

        ReSet Collision_Avoidance;
        ConfL\Off;
        WaitSyncTask syncpoint,tasklist;
        !origL := CRobT(\Tool:=tCamL_orig);
        
        MoveToDist distances{3},nRadius{1}\sp:=v100, wobjHeart;
    ENDPROC

    
    PROC L_update()
        VAR robtarget new;
        VAR pose orig_pose;
        VAR pose new_pose;
        VAR pose diff;
        VAR pose tool_pose;
        VAR btnres answer;
        tool_pose := tCamL_orig.tframe;
        new := CRobT(\Tool:=tCamL_orig);
        orig_pose := [origL.trans, origL.rot];
        new_pose := [new.trans, new.rot];
        diff := PoseMult(PoseInv(new_pose), orig_pose);
        tCamL.tframe := PoseMult(tool_pose, diff);
    
        
    ENDPROC
    
    
    PROC R_update()
    ENDPROC

    PROC reset_tool()
        tCamL := tCamL_orig;
        
    ENDPROC

    PROC gotoX2()
        ReSet Collision_Avoidance;
        ConfL\Off;
        WaitSyncTask syncpoint,tasklist;
        MoveToDist distances{15},nRadius{1}\sp:=v100, wobjHeart;

    ENDPROC


    PROC goto1100()
        ReSet Collision_Avoidance;
        ConfL\Off;
        WaitSyncTask syncpoint,tasklist;
        MoveToDist distances{1},nRadius{1}\sp:=v100, wobjHeart;

    ENDPROC




    PROC goto1400()
        ReSet Collision_Avoidance;
        ConfL\Off;
        WaitSyncTask syncpoint,tasklist;
        MoveToDist distances{1},nRadius{2}\sp:=v100, wobjHeart;

    ENDPROC


    PROC run1100()
        runtest convergencePos{1},nRadius{1};
    ENDPROC

    PROC run1400()
        
        runtest convergencePos{2},nRadius{2};
    ENDPROC



    PROC runtest(pos position,num h)
        ReSet Collision_Avoidance;
        ConfL\Off;
        WaitSyncTask syncpoint,tasklist;

        MoveToDist distances{1},h\sp:=v100, wobjHeart;
        
        FOR i FROM 1 TO Dim(distances,1) DO
            WaitSyncTask syncpoint,tasklist;
            MoveToDist distances{i},h, wobjHeart;
            WaitTime nwaittime;
        ENDFOR
        
        WaitSyncTask syncpoint,tasklist;
    ENDPROC

ENDMODULE
