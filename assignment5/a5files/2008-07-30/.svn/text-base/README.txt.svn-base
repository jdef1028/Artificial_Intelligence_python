Sketch Recognition Tools README

Christine Alvarado

James Brown, Eric Doi, Martin Field, Emily Fujimoto, and Sketchers 2006-2008

Harvey Mudd College
sketchers@cs.hmc.edu

All code is licensed under the GNU General Public License unless otherwise
noted. The text of the GPL can be found in the file GPL.txt in the root 
directory of this project.

Source is available on-demand.

******************************

Included Programs:

In the Programs\ directory, you will find compiled versions of our Labeler
and SketchPanel tools. 

The Labeler is a program for viewing Microsoft
Windows Journal, MIT XML, or DRS files. It supports labeling of strokes,
fragmentation, grouping, feature viewing, and conversion to MIT XML format.
The labeler makes use of Domain files for colorization and labeling; several
of these files can be found in the Domains\ directory, and their file format
is explained below.

SketchPanel is a testbed for a possible end-user UI which allows the user to
draw a symbol, have it recognized, and save it. The only recognition engine
currently supported is the SVM-based GateRecognizer, which has somewhat...
lackluster results.

******************************

Domain Files

Domain files are text (.txt) files of the format:

<name of research group>
<name of domain>
<label> <priority number> <color>
<label> <priority number> <color> ...

Example:

HMC Research 07
Test Wire/Gate Logic Diagram
Wire 0 Blue
Gate 1 Red


******************************

MIT XML Format


Sketches are stored hierarchically:
   * Points are the smallest unit
   * Substrokes are Shapes that are groups of points. They are primitive lines and arcs.
   * Strokes are Shapes that are groups of substrokes.
   * Other Shapes are labels that groups of substroke together with a type (e.g. "And", "Or")


Point
   * Attributes:
      * x: (double) x coordinate
      * y: (double) y coordinate
      * pressure: (int) Pressure for the point (0-255 on Tablet PC)
      * time: (unsigned long) Time point was created in milliseconds since 1/1/1970 UTC
      * id: (GUID) Identifying Guid for the point
      * name: (string) Name of the point

   * Example:
      <point x="6150" y="2374" pressure="127" time="1157483794277" name="point" id="1faa972c-78cd-4221-9609-e7cb784c4f50" />   


Shape
   * Sub-Elements:
      * arg: The components of the shape (e.g., Points that are in the Stroke)
      * alias: The aliases of the shape (names for the components that are used in the language)
   
   * Attributes:
      * id: (GUID) Shape ID
      * name: (string) Name of the shape
      * time: (unsigned long) Time shape was created in milliseconds since 1/1/1970 UTC. Creation time is recorded as the time when the user finally lifts the stylus.
      * type: (string) The type of the shape (e.g., "Stroke")
      * author: (GUID) Id of the author of the stroke
      * color: (RGBA integer) RGBA representation of the color
      * height: (int) Used for the height of a shape
      * width: (int) Used for the width of a shape
      * laysInk: (boolean) If true render the shape, if false, don't.
      * penTip: "Rectangle" or "Ball". The pen tip type.
      * raster: "MaskPen" or "CopyPen". How to render the ink.
      * x: (int) Top left origin, x
      * y: (int) Top left origin, y
      * leftx: (int) Top left origin, x. This is redundant.
      * topy: (int) Top left origin, y. This is redundant.
      * start: (GUID) Starting argument (point, substroke, etc.) based on time
      * end: (GUID) Ending argument based on time
      * source: (string) Where the shape was created

   * Examples:
   <shape type="substroke" name="substroke" id="a6ed61dc-09fc-4370-910b-ff59c5a94d80" time="1157483750968" x="2032" y="1318" color="-16777216" height="651" width="402" penTip="Ball" raster="CopyPen" leftx="2032" topy="1318" start="020113db-580f-488c-94b1-507b35cd0273" end="98900040-af33-4349-b0ac-7423bfa43231" source="Converter">
      <arg type="point">020113db-580f-488c-94b1-507b35cd0273</arg> 
      <arg type="point">3c91af04-edb3-4905-80a0-e5443fce18ef</arg> 
      ...

   <shape type="stroke" name="stroke" id="b96f38c3-c34e-4642-941a-a5b17ef89071" time="1157483794843" source="Converter">
      <arg type="substroke">bef43cdb-a10b-49e0-b42c-104fa143021d</arg>
      ...

******************************
