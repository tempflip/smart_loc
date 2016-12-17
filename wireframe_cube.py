"""
 Wireframe 3D cube simulation.
 Developed by Leonel Machava <leonelmachava@gmail.com>

 http://codeNtronix.com
"""
import sys, math, pygame
from pygame.locals import *
import ip_webcam

class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)
 
    def rotateX(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)
 
    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)
 
    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)
 
    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, 1)

class Simulation:
    def __init__(self, win_width = 640, win_height = 480):
        pygame.init()

        self.screen = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption("3D Wireframe Cube Simulation (http://codeNtronix.com)")
        
        self.clock = pygame.time.Clock()

        self.vertices = [
            Point3D(-0.4,1,-0.1),
            Point3D(0.4,1,-0.1),
            Point3D(0.4,-1,-0.1),
            Point3D(-0.4,-1,-0.1),
            Point3D(-0.4,1,0.1),
            Point3D(0.4,1,0.1),
            Point3D(0.4,-1,0.1),
            Point3D(-0.4,-1,0.1)
        ]

        # Define the vertices that compose each of the 6 faces. These numbers are
        # indices to the vertices list defined above.
        self.faces = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)]

        self.angleX, self.angleY, self.angleZ = 0, 0, 0
        
    def run(self):

        TO_DEG = 57.2958

        cam = ip_webcam.ip_webcam(endpoint = 'http://192.168.1.102:8080/sensors.json', sense=['gyro', 'rot_vector'])

        FPS = 50
        sense_ticker = 0
        sense_per_frame = 6
        rot_multipl = 8

        timestamp = 0
        last_timestamp = 0
        """ Main Loop """

        adjustX = 0
        adjustY = 0
        adjustZ = 0

        rot_axis_x = 1
        rot_axis_y = 1
        rot_axis_z = 1

        while 1:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()


            # do a sense
            if sense_ticker == 0:
                gyro_data = cam.sense_async()
            
            if cam.sense_avail():
                sense = cam.sense_pop()
                
                timestamp = sense['gyro'][0]
                dt = timestamp - last_timestamp
                last_timestamp = timestamp

                gyro_x, gyro_y, gyro_z = sense['gyro'][1]
                rot_x, rot_y, rot_z, rot_cos, acc = sense['rot_vector'][1]

                rot_axis, angle = ip_webcam.calc_rot(rot_x, rot_y, rot_z, rot_cos)

                rot_axis_x = rot_axis[0]
                rot_axis_y = rot_axis[1]
                rot_axis_z = rot_axis[2]

                (alpha, beta) = ip_webcam.rot_axis_to_angle(rot_axis_x, rot_axis_y, rot_axis_z)

                #print "rot_x: {}, rot_y: {}, rot_z: {}".format(gyro_x, gyro_y, gyro_z)
                #print "rot_axis x:{} angle: {}".format(rot_axis, angle)
                print "alpha {} beta {} gamma {} ".format(alpha * TO_DEG, beta * TO_DEG, angle * TO_DEG)


                self.angleX = alpha * TO_DEG  - adjustX
                self.angleY = angle * TO_DEG - adjustY
                self.angleZ = beta * TO_DEG - adjustZ



            #print gyro_data

            #timestamp = gyro_data[0]
            #gyro_y = gyro_data[1][1]

            #self.angleY += gyro_y

            #print timestamp, gyro_y
            sense_ticker += 1
            sense_ticker %= (FPS / sense_per_frame)


            keys = pygame.key.get_pressed()
            if keys[K_DOWN] :
                self.angleX += 1

            if keys[K_UP] :
                self.angleX -= 1

            if keys[K_LEFT] :
                self.angleY -= 1

            if keys[K_RIGHT] :
                self.angleY += 1

            if keys[K_m] :
                self.angleZ += 1

            if keys[K_n] :
                self.angleZ -= 1

            if keys[K_SPACE] :
                adjustX = self.angleX
                adjustY = self.angleY
                adjustZ = self.angleZ

            self.clock.tick(FPS)
            self.screen.fill((0,0,0))

            #rot_axis_start = Point3D(x = 0, y = 0, z = 0).project(self.screen.get_width(), self.screen.get_height(), 256, 4)
            #rot_axis_end = Point3D(x = rot_axis_x * 4, y = rot_axis_x * 4, z = rot_axis_z * 4).project(self.screen.get_width(), self.screen.get_height(), 256, 4)


            #pygame.draw.line(self.screen, (255, 10, 10), (rot_axis_start.x, rot_axis_start.y), (rot_axis_end.x, rot_axis_end.y))

            # Will hold transformed vertices.
            t = []
            
            for v in self.vertices:
                # Rotate the point around X axis, then around Y axis, and finally around Z axis.
                r = v.rotateX(self.angleX).rotateY(self.angleY).rotateZ(self.angleZ)
                # Transform the point from 3D to 2D
                p = r.project(self.screen.get_width(), self.screen.get_height(), 256, 4)
                # Put the point in the list of transformed vertices
                t.append(p)

            for f in self.faces:
                pygame.draw.line(self.screen, (255,255,255), (t[f[0]].x, t[f[0]].y), (t[f[1]].x, t[f[1]].y))
                pygame.draw.line(self.screen, (255,255,255), (t[f[1]].x, t[f[1]].y), (t[f[2]].x, t[f[2]].y))
                pygame.draw.line(self.screen, (255,255,255), (t[f[2]].x, t[f[2]].y), (t[f[3]].x, t[f[3]].y))
                pygame.draw.line(self.screen, (255,255,255), (t[f[3]].x, t[f[3]].y), (t[f[0]].x, t[f[0]].y))
            
            pygame.display.flip()

if __name__ == "__main__":
    Simulation().run()
