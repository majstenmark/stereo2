MODULE Data

    ! Tooldata for the right camera. 
    TASK PERS tooldata tCamR:=[TRUE,[[-55.3,0,21.2],[1,0,0,0]],[0.23,[-55.3,0,21.2],[1,0,0,0],0,0,0]];
    TASK PERS tooldata tCamR_orig:=[TRUE,[[-55.3,0,21.2],[1,0,0,0]],[0.23,[-55.3,0,21.2],[1,0,0,0],0,0,0]];
    
    TASK PERS robtarget origR := [[456,35,1099.44],[0.491981,0.507892,0.491981,0.507892],[1,2,0,4],[165,9E+9,9E+9,9E+9,9E+9,9E+9]];
    !Additional rotational adjustments
    VAR num x_offs:=0.0;
    VAR num y_offs:=0;!0.12;
    VAR num z_offs:=0;!-1.00;
    
    !Data for the experiment
    VAR num distances{20}:=[50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240];
    
    PERS num nWaittime:=5;
    PERS wobjdata wobjHeart:=[FALSE,TRUE,"",[[0,0,-900],[1,0,0,0]],[[0,0,0],[1,0,0,0]]];
    PERS speeddata speedSlow:=[50,50,5000,5000];
    PERS num nRadius{2}:=[1100, 1400];
    PERS pos convergencePos{2} := [[0, 0, 0], [0, 0, -300]]; !z will be added to this position!

    !Adjusting the x and z position of the convergence points.
    PERS num x:= 456;
    PERS num z:= -600; !1550;
    
    
    
    !For synchronization
    PERS tasks tasklist{2}:=[["T_ROB_R"],["T_ROB_L"]];
    VAR syncident syncpoint;
    
    !The Stereo2 app reads this status message and displays it on the Flexpendant.
    PERS string myStatus:="Dist 240 h = 1400";
    
    
    !For moving into a raised position and to resting aka 'bat' position
    VAR syncident syncraise;
    VAR syncident syncbat1;
    VAR syncident syncbat2;
    VAR jointtarget jtraised:=[[66.0331,-85.1911,41.3253,139.052,44.5799,5.71225],[-62.1903,9E+09,9E+09,9E+09,9E+09,9E+09]];
    VAR jointtarget jtbat:=[[64.6304,-143.384,34.5095,60.7933,53.7269,8.84934],[-140.721,9E+09,9E+09,9E+09,9E+09,9E+09]];
    VAR jointtarget jtraisedVia:=[[70.951,-118.367,40.9926,106.328,50.1338,-20.9947],[-83.9002,9E+09,9E+09,9E+09,9E+09,9E+09]];
    TASK PERS tooldata tool1:=[TRUE,[[-49.461,-63.6951,27.321],[1,0,0,0]],[0.23,[-49.461,-63.6951,27.321],[1,0,0,0],0,0,0]];
    PERS tooldata tMarker:=[TRUE,[[0,0,14],[1,0,0,0]],[0.001,[0,0,0.001],[1,0,0,0],0,0,0]];
    TASK PERS tooldata camup:=[TRUE,[[-55.3,0,21.2],[1,0,0,0]],[0.23,[-55.3,0,21.2],[1,0,0,0],0,0,0]];
    PERS wobjdata woupsidedown:=[FALSE,TRUE,"",[[0,0,820],[0,1,0,0]],[[0,0,0],[1,0,0,0]]];
    PERS wobjdata wobj0New:=[FALSE,TRUE,"",[[0,0,820],[0,0,1,0]],[[0,0,0],[1,0,0,0]]];
    TASK PERS wobjdata flangeRobL:=[FALSE,FALSE,"ROB_L",[[173.578467213,84.619790784,0.000800546],[0,-0.000002743,-0.000003834,1]],[[0,0,0],[1,0,0,0]]];
    TASK PERS wobjdata flangeRobR:=[FALSE,FALSE,"ROB_R",[[-171.357658985,86.166016842,-0.356297018],[0,-0.002091433,-0.000024218,0.999997813]],[[0,0,0],[1,0,0,0]]];
        

ENDMODULE