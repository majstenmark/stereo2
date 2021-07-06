MODULE MainModule

    


    PROC Main()
        runall;
    ENDPROC

    PROC goToCalibPos()
        VAR jointtarget calibPos := [[-0.00840108,-129.997,30.0284,-0.019315,40.0852,-0.0138285],[-135.001,9E+09,9E+09,9E+09,9E+09,9E+09]];
        MoveAbsJ calibPos\NoEOffs,v1000,z50,tool0;
    ENDPROC
    
    PROC runall()
        
        FOR i FROM 1 TO DIM(nRadius, 1) DO
            runtest convergencePos{i}, nRadius{i};
        ENDFOR
    ENDPROC



    PROC MoveToDist(num dist,num h\speeddata sp, PERS wobjdata wobjHeart)
        VAR robtarget position:=[[365,-10,1000],[0.5,0.5,0.5,0.5],[1,-2,-2,4],[165,9E+09,9E+09,9E+09,9E+09,9E+09]];
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

        position.trans:=[x,y,zh];
        IF Present(sp) THEN
            speed:=sp;
        ENDIF

        MoveL RelTool(position,0,0,0\Rx:=x_offs\Ry:=y_offs\Rz:=-(angle+z_offs)),speed,fine,tCamR\WObj:=wobjHeart;

    ENDPROC


    PROC inc()
        VAR num s:=1;
        z := z + s;
        goto1100;
    ENDPROC


    PROC incinc()

        VAR num s:=5;
        z := z + s;
        goto1100;
    ENDPROC


    PROC dec()
        
        VAR num s:=-1;
        z := z + s;
        goto1100;
    ENDPROC


    PROC decdec()
        VAR num s:=-5;
        z := z + s;
        goto1100;
    ENDPROC

    PROC incX()
        VAR num s:=1;
        x:=x+s;
        goto1100;
    ENDPROC


    PROC incincX()

        VAR num s:=5;
        x:=x+s;
        goto1100;
    ENDPROC


    PROC decX()
        
        VAR num s:=-1;
        x:=x+s;
        goto1100;
    ENDPROC


    PROC decdecX()

        VAR num s:=-5;
        x:=x+s;
        goto1100;
    ENDPROC

    PROC gotoX1()
        ReSet Collision_Avoidance;
        ConfL\Off;
        wobjHeart.uframe.trans := [convergencePos{1}.x, convergencePos{1}.y, convergencePos{1}.z + z];
        WaitSyncTask syncpoint,tasklist;
        !origR := CRobT(\Tool:=tCamR_orig);
        MoveToDist distances{3},nRadius{1}\sp:=v100, wobjHeart;
    ENDPROC

    PROC L_update()
       
    ENDPROC
    
    
    PROC R_update()
        VAR robtarget new;
        VAR pose orig_pose;
        VAR pose new_pose;
        VAR pose diff;
        VAR pose tool_pose;
        VAR btnres answer;
        tool_pose := tCamR_orig.tframe;
        new := CRobT(\Tool:=tCamR_orig);
        orig_pose := [origR.trans, origR.rot];
        new_pose := [new.trans, new.rot];
        diff := PoseMult(PoseInv(new_pose), orig_pose);
        tCamR.tframe := PoseMult(tool_pose, diff);
    
        
    ENDPROC

    PROC reset_tool()
        tCamR := tCamR_orig;
        
    ENDPROC

    PROC gotoX2()
        
        ReSet Collision_Avoidance;
        ConfL\Off;
        wobjHeart.uframe.trans := [convergencePos{1}.x, convergencePos{1}.y, convergencePos{1}.z+z];
        WaitSyncTask syncpoint,tasklist;
        MoveToDist distances{15},nRadius{1}\sp:=v100, wobjHeart;

    ENDPROC


    PROC gofrombatpos()

        ReSet Collision_Avoidance;
        ConfL\Off;
        MoveAbsJ jtraisedVia\NoEOffs,v100,fine,tCamR;
        MoveAbsJ jtraised\NoEOffs,v100,fine,tCamR;
        WaitSyncTask syncraise,tasklist;
    ENDPROC

    PROC gotoraisedpos()
        ReSet Collision_Avoidance;
        ConfL\Off;
        MoveAbsJ jtraised\NoEOffs,v100,fine,tCamR;
        WaitSyncTask syncraise,tasklist;

    ENDPROC

    PROC gotobatpos()
        ReSet Collision_Avoidance;
        ConfL\Off;
        MoveAbsJ jtraised\NoEOffs,v100,fine,tCamR\WObj:=wobjHeart;
        WaitSyncTask syncbat1,tasklist;
        WaitSyncTask syncbat2,tasklist;
        MoveAbsJ jtraisedVia\NoEOffs,v100,fine,tCamR;
        MoveAbsJ jtbat\NoEOffs,v100,fine,tCamR;

    ENDPROC



    PROC goto1100()
        ReSet Collision_Avoidance;
        ConfL\Off;
        wobjHeart.uframe.trans := [convergencePos{1}.x, convergencePos{1}.y, convergencePos{1}.z + z];    
        WaitSyncTask syncpoint,tasklist;
        MoveToDist distances{1},nRadius{1}\sp:=v100, wobjHeart;
    ENDPROC


    PROC goto1400()
        ReSet Collision_Avoidance;
        ConfL\Off;
        wobjHeart.uframe.trans := [convergencePos{2}.x, convergencePos{2}.y, convergencePos{2}.z + z];
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

        ConfL\Off;
        wobjHeart.uframe.trans:=[position.x, position.y, position.z + z];
        WaitSyncTask syncpoint,tasklist;
        ReSet Collision_Avoidance;
        MoveToDist distances{1},h\sp:=v100, wobjHeart;
        
        FOR i FROM 1 TO Dim(distances,1) DO
            
            WaitSyncTask syncpoint,tasklist;
            myStatus:="Dist "+NumToStr(distances{i},0)+" h = "+NumToStr(h,0);
            ErrWrite\I,"Started moving. Dist "+NumToStr(distances{i},0)+" h = "+NumToStr(h,0),"";
            MoveToDist distances{i},h, wobjHeart;
            WaitTime nwaittime;
        ENDFOR
        WaitSyncTask syncpoint,tasklist;
    ENDPROC


ENDMODULE
