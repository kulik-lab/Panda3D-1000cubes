from __future__ import print_function

import os
import sys
from panda3d.core import Vec3, load_prc_file_data, Material
from direct.showbase.ShowBase import ShowBase

from panda3d.core import *
import simplepbr
from random import randint
from math import sin

# Change to the current directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Insert the pipeline path to the system path, this is required to be
# able to import the pipeline classes
pipeline_path = "../../"

# Just a special case for my development setup, so I don't accidentally
# commit a wrong path. You can remove this in your own programs.
if not os.path.isfile(os.path.join(pipeline_path, "setup.py")):
    pipeline_path = "../../RenderPipeline/"

sys.path.insert(0, pipeline_path)

# Import the render pipeline class
from rpcore import RenderPipeline

# This is a helper class for better camera movement - see below.
from rpcore.util.movement_controller import MovementController


class Application(ShowBase):
    def __init__(self):
        # Setup window size and title
        load_prc_file_data("", """
            # win-size 1600 900
            window-title Render Pipeline - Material Sample
        """)

        # Construct the render pipeline
        self.render_pipeline = RenderPipeline()
        self.render_pipeline.create(self)
        self.render_pipeline.daytime_mgr.time = "14:30"


        # Load the scene
        model = self.loader.load_model("models/environment")
        model.reparent_to(self.render)

        self.render_pipeline.prepare_scene(model)
 
        # Initialize movement controller, this is a convenience class
        # to provide an improved camera control compared to Panda3Ds default
        # mouse controller.
        self.controller = MovementController(self)
        self.controller.set_initial_position_hpr(
            Vec3(-37.2912578583, -23.290019989, 16.88211250305),
            Vec3(-39.7285499573, -14.6770210266, 0.0))
        self.controller.setup()

        self.start=False
        self.s=0
        self.n = 0
        self.nodes = []
        for j in range(10):
            for i in range(100):
                print(j,i)
                self.nodes.append(loader.loadModel("scene/color_cube_1.gltf"))
                self.nodes[self.n].setPos(i*3,j*3,0)
                self.nodes[self.n].setAntialias(AntialiasAttrib.MAuto)
                self.nodes[self.n].reparentTo(self.render)
                self.n = self.n + 1

        self.taskMgr.add(self.update, "update")

    def update(self, task):
        self.s= self.s+1
        if self.s > 320: 
            self.s = 0
        for i in range (999):
            self.nodes[i].setPos( 0.002*i*sin((2*i+self.s)/25), 0.002*i*sin((i+self.s)/25),0.01*sin(0.1*self.s)+2.1*i+2)
            self.nodes[i].setHpr(360*sin((i+self.s)/100),0,0)
        return task.cont



Application().run()
