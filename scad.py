import copy
import opsc
import oobb
import oobb_base
import yaml
import os
import scad_help

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    parts = []

    typ = kwargs.get("typ", "")

    if typ == "":
        #setup    
        #typ = "all"
        typ = "fast"
        #typ = "manual"

    oomp_mode = "project"
    #oomp_mode = "oobb"

    test = False
    #test = True

    if typ == "all":
        filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = True; test = False
        #default
        #filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = True; test = False
    elif typ == "fast":
        filter = ""; save_type = "none"; navigation = False; overwrite = True; modes = ["3dpr"]; oomp_run = False
        #default
        #filter = ""; save_type = "none"; navigation = False; overwrite = True; modes = ["3dpr"]; oomp_run = False
    elif typ == "manual":
    #filter
        filter = ""
        #filter = "test"

    #save_type
        save_type = "none"
        #save_type = "all"
        
    #navigation        
        #navigation = False
        navigation = True    

    #overwrite
        overwrite = True
                
    #modes
        #modes = ["3dpr", "laser", "true"]
        modes = ["3dpr"]
        #modes = ["laser"]    

    #oomp_run
        oomp_run = True
        #oomp_run = False    

    #adding to kwargs
    kwargs["filter"] = filter
    kwargs["save_type"] = save_type
    kwargs["navigation"] = navigation
    kwargs["overwrite"] = overwrite
    kwargs["modes"] = modes
    kwargs["oomp_mode"] = oomp_mode
    kwargs["oomp_run"] = oomp_run
    
       
    # project_variables
    if True:
        pass
    
    # declare parts
    if True:

        directory_name = os.path.dirname(__file__) 
        directory_name = directory_name.replace("/", "\\")
        project_name = directory_name.split("\\")[-1]
        #max 60 characters
        length_max = 40
        if len(project_name) > length_max:
            project_name = project_name[:length_max]
            #if ends with a _ remove it 
            if project_name[-1] == "_":
                project_name = project_name[:-1]
                
        #defaults
        kwargs["size"] = "oobb"
        kwargs["width"] = 1
        kwargs["height"] = 1
        kwargs["thickness"] = 3
        #oomp_bits
        if oomp_mode == "project":
            kwargs["oomp_classification"] = "project"
            kwargs["oomp_type"] = "github"
            kwargs["oomp_size"] = "oomlout"
            kwargs["oomp_color"] = project_name
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""
        elif oomp_mode == "oobb":
            kwargs["oomp_classification"] = "oobb"
            kwargs["oomp_type"] = "part"
            kwargs["oomp_size"] = ""
            kwargs["oomp_color"] = ""
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""

        part_default = {} 
       
        part_default["project_name"] = project_name
        part_default["full_shift"] = [0, 0, 0]
        part_default["full_rotations"] = [0, 0, 0]
        
        part = copy.deepcopy(part_default)
        p3 = copy.deepcopy(kwargs)
        p3["width"] = 9
        p3["height"] = 7
        p3["thickness"] = 39
        #p3["extra"] = ""
        part["kwargs"] = p3
        nam = "base"
        part["name"] = nam
        if oomp_mode == "oobb":
            p3["oomp_size"] = nam
        if not test:
            pass
            parts.append(part)


    kwargs["parts"] = parts

    scad_help.make_parts(**kwargs)

    #generate navigation
    if navigation:
        sort = []
        #sort.append("extra")
        sort.append("name")
        sort.append("width")
        sort.append("height")
        sort.append("thickness")
        
        scad_help.generate_navigation(sort = sort)

def get_base(thing, **kwargs):
    prepare_print = kwargs.get("prepare_print", True)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    

    depth_base = 6


    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth_base
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add straps
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_plate"
    p3["depth"] = depth
    p3["width"] = width - 1.5
    p3["height"] = 1
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    poss = []
    shift_y = 3/2 * 15
    pos11 = copy.deepcopy(pos1)    
    pos11[1] += -shift_y
    pos12 = copy.deepcopy(pos1)
    pos12[1] += shift_y
    poss.append(pos11)
    poss.append(pos12)
    p3["pos"] = poss
    oobb_base.append_full(thing,**p3)

    
    


    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = ["top", "bottom"]
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    #add screws for base
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_screw_countersunk"
        p3["radius_name"] = "m3_screw_wood"
        p3["depth"] = depth_base
        p3["m"] = "#"
        poss = []
        if True:
            pos1 = copy.deepcopy(pos)
            pos1[2] += depth_base
            shift_y = (height-2)/2 * 15
            shift_x = (width-1)/2 * 15
            pos11 = copy.deepcopy(pos1)
            pos11[0] += -shift_x
            pos11[1] += shift_y
            pos12 = copy.deepcopy(pos1)
            pos12[0] += shift_x
            pos12[1] += shift_y
            pos13 = copy.deepcopy(pos1)
            pos13[0] += -shift_x
            pos13[1] += -shift_y
            pos14 = copy.deepcopy(pos1)
            pos14[0] += shift_x
            pos14[1] += -shift_y
            poss.append(pos11)
            poss.append(pos12)
            poss.append(pos13)
            poss.append(pos14)
        p3["pos"] = poss
        oobb_base.append_full(thing,**p3)

    #add screws for joiner
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_screw_socket_cap"
        p3["radius_name"] = "m3"
        p3["nut"] = True
        p3["overhang"] = True
        p3["depth"] = depth - 5
        p3["clearance"] = ["top","bottom"]
        p3["m"] = "#"
        p3["zz"] = "top"
        poss = []
        if True:
            pos1 = copy.deepcopy(pos)
            pos1[2] += depth
            shift_x = (width-2)/2 * 15
            shift_y = 3/2*15
            pos11 = copy.deepcopy(pos1)
            pos11[0] += -shift_x
            pos11[1] += shift_y
            pos12 = copy.deepcopy(pos1)
            pos12[0] += shift_x
            pos12[1] += shift_y
            pos13 = copy.deepcopy(pos1)
            pos13[0] += -shift_x
            pos13[1] += -shift_y
            pos14 = copy.deepcopy(pos1)
            pos14[0] += shift_x
            pos14[1] += -shift_y
            poss.append(pos11)
            poss.append(pos12)
            poss.append(pos13)
            poss.append(pos14)
        p3["pos"] = poss
        oobb_base.append_full(thing,**p3)


    #add charger_cutout
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = f"cube"
    #p3["radius"] = 5
    clear = 0.25
    wid =  94 + clear
    hei = 101 + clear
    dep = 29 + clear
    size = [wid, hei, dep]
    p3["size"] = size
    p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[0] += -wid/2
    pos1[1] += -hei/2
    pos1[2] += 6
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 150
        pos1[1] += 0
        pos1[2] += depth_base * 2
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0
        pos1[1] += 0
        pos1[2] += depth_base#-500/2        
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)
    
if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)