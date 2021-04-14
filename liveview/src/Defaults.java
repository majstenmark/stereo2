import java.io.*;
import java.util.*;
public class Defaults {
    String prefix_save;
    int no_cams;
    int exposure_time;
    int downsample = 1;
    String command;
    boolean debayer = true;
    int[] LUT;
    public Defaults() {
    }

    public static Defaults get(List<String> args){
        Defaults def;
        if(args.contains("mock"))
            def = Defaults.mock();
        else if(args.contains("slave"))
            def = Defaults.slave();
        else if(args.contains("usb"))
            def = Defaults.all_master(2, false);
        else if(args.contains("axis"))
            def = Defaults.axis();
        else if(args.contains("all-master"))
            def = Defaults.all_master(7, true);
        else
            def = Defaults.production();
        def.LUT = Util.get_LUT(!args.contains("mock"));
        return def;
    }

    public static Defaults production(){
        Defaults d = new Defaults();
        d.prefix_save = ".";
        d.no_cams = 7;
        d.exposure_time = 4000;
        d.downsample = 2;
        d.command = "python3 python/capture_ximea.py --one_master --convert_id --id %d --start %d --downsample %d --exposure %d";
        return d;
    }
    public static Defaults mock(){
        Defaults d = new Defaults();
        d.prefix_save = ".";
        d.no_cams = 2;
        d.exposure_time = 10000;
        d.command = "python3 python/mock2.py --id %d --start %d --downsample %d --exposure %d";
        return d;
    }
    public static Defaults slave(){
        Defaults d = new Defaults();
        d.prefix_save = ".";
        d.no_cams = 7;
        d.exposure_time = 5000;
        d.downsample = 2;
        d.command = "python3 python/capture_ximea.py --all_slave --convert_id --id %d --start %d --downsample %d --exposure %d";
        return d;
    }
    public static Defaults all_master(int no_cams, boolean convert_id){
        Defaults d = new Defaults();
        d.prefix_save = ".";
        d.no_cams = no_cams;
        d.exposure_time = 5000;
        d.downsample = 2;
        String add = convert_id? "--convert_id" : "";
        d.command = "python3 python/capture_ximea.py --all_master " + add + " --id %d --start %d --downsample %d --exposure %d";
        return d;
    }
    public static Defaults axis(){
        Defaults d = new Defaults();
        d.prefix_save = ".";
        d.no_cams = 2;
        d.exposure_time = 5000;
        d.downsample = 2;
        d.command = "python3 python/axis_impl.py --id %d --start %d --downsample %d --exposure %d";
        d.debayer = false;
        return d;
        
    }
}
