
    MODULE Data

        
    ! Tooldata for the left camera.
    TASK PERS tooldata tCamL:=[TRUE,[[55.3,0,21.2],[1,0,0,0]],[0.23,[55.3,0,21.2],[1,0,0,0],0,0,0]];
    TASK PERS tooldata tCamL_orig:=[TRUE,[[55.3,0,21.2],[1,0,0,0]],[0.23,[55.3,0,21.2],[1,0,0,0],0,0,0]];
    
    TASK PERS robtarget origL := [[456,-35,1099.44],[0.491981,0.507892,0.491981,0.507892],[-1,2,-2,4],[-163.142,9E+9,9E+9,9E+9,9E+9,9E+9]];
    
   ! Additional rotational adjustments. 
    VAR num x_offs:= 0.0;
    VAR num y_offs:= 0.0;
    VAR num z_offs:=0;!0.43;
    
    
    !Data for the experiment. These are shared with the right task and assigned in T_ROB_R/Data
    VAR num distances{20}:=[50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240];
    PERS num nWaittime;
    PERS wobjdata wobjHeart;
    PERS speeddata speedSlow;
    PERS num nRadius{2};
    PERS pos convergencePos{2};
    
    
    !Adjusting the x and z position of the convergence points.
    PERS num x;
    PERS num z;
    
    
    
    !For synchronization
    PERS tasks tasklist{2}:=[["T_ROB_R"],["T_ROB_L"]];
    VAR syncident syncpoint;
    
    !For moving into a raised position and to resting aka 'bat' position
    VAR jointtarget jtraised:=[[-74.7004,-91.3236,43.3868,218.306,45.6835,-171.438],[61.909,9E+09,9E+09,9E+09,9E+09,9E+09]];
    VAR syncident syncraise;
    VAR syncident syncbat1;
    VAR syncident syncbat2;
    VAR jointtarget jtbat:=[[-56.5752,-119.517,21.4015,271.499,49.3732,-213.567],[155.307,9E+09,9E+09,9E+09,9E+09,9E+09]];

ENDMODULE