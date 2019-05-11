// Flipotronics V1
// San Jose, 5/4/2019, 
showSide = true;
$fn=60;
HP = 5.08;
U3 = 133.4;
thick = 6.45;
plateWidth = 20;
rackSteelLength = 84 * HP;

length = 260;
height = 225;
radius = 0;

// left panel




translate([0, 0, 0]){ 
    difference(){
        roundedBox(length, plateWidth, height);
         rotate([43, 0, 0]){
            translate([0, 10, 0]){ 
                roundedBox(length*2, plateWidth*2, height*2);
            }
        }   
    }
}
color([1,0,0])
translate([0, 55, 45]){ 
        rotate([0,90,0]){
            cylinder(h=plateWidth, d1=90, d2=90, center=false);
        }
}

// right panel
if(showSide){
color([1,1,0])
translate([plateWidth + rackSteelLength, 0, 0]){ 
    roundedBox(length, plateWidth, height);
}
}

//front wood
translate([plateWidth , 60-thick-8, 0]){ 
    roundedBox(thick, rackSteelLength, 90);
}

//back wood
translate([0 , 260, 40]){ 
    roundedBox(thick, rackSteelLength+40, 185);
}

//top wood
translate([plateWidth , 222, 225-thick]){ 
    roundedBox(38, rackSteelLength, thick);
}

//rack metal
color([1,0,0])
translate([plateWidth , 60-8, 90-23]){ 
    roundedBox(8, rackSteelLength, 23);
}


//rack metal 2
color([1,0,0])
translate([plateWidth , 60 + 130-8, 90-23]){ 
    roundedBox(8, rackSteelLength, 23);
}


//rack wood 1
color([1,0,1])
translate([plateWidth , 60 + 147, 87]){ 
     rotate([76,00,0]){
        roundedBox(16, rackSteelLength, 16);
     }
}

//rack wood 2
color([1,0,1])
translate([plateWidth , 236, 200]){ 
    rotate([76,00,0]){
        roundedBox(16, rackSteelLength, 16);
    }
}



//floor
translate([plateWidth , 75, 0]){ 
    roundedBox(185, rackSteelLength, 7);
}

// PI
color([0,1,0])
translate([25 , 185, thick]){ 
    roundedBox(75, 104, 23);
}


// Arduino
color([0,1,0])
translate([200 , 185, thick]){ 
    roundedBox(54, 69, 25);
}

// Power
color([0,1,0])
translate([335 , 185, thick]){ 
    roundedBox(60, 100, 25);
}


// Foot
color([0,0,0])
translate([10 , 10, -5]){ 
   cylinder(h=5, d1=20, d2=20, center=false);
}
color([0,0,0])
translate([10 , 250, -5]){ 
   cylinder(h=5, d1=20, d2=20, center=false);
}
color([0,0,0])
translate([457 , 10, -5]){ 
   cylinder(h=5, d1=20, d2=20, center=false);
}
color([0,0,0])
translate([457 , 250, -5]){ 
   cylinder(h=5, d1=20, d2=20, center=false);
}




module roundedBox(length, width, height)
{

    //base rounded shape
    minkowski() {
        cube(size=[width,length, height]);
        cylinder(r=radius, h=1);
    }
  
    
}