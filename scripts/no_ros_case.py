import carla
import random
import time

# Connect to the client and retrieve the world object
client = carla.Client('localhost', 2000)

# Longer timeout for Town12
client.set_timeout(30.0)

world = client.get_world()

print("Loading town")
# client.load_world('Town05')
client.load_world('Town12')
print("Done loading town")

# Get the vehicle blueprint
ego_bp = world.get_blueprint_library().find('vehicle.tesla.model3')
ego_bp.set_attribute('role_name','ego_vehicle')

# Get the map's spawn points
spawn_points = world.get_map().get_spawn_points()

ego_vehicle = world.spawn_actor(ego_bp, random.choice(spawn_points))

# Create a transform to place the camera on top of the vehicle
camera_init_trans = carla.Transform(carla.Location(z=1.5))

# We create the camera through a blueprint that defines its properties
camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')

# We spawn the camera and attach it to our ego vehicle
camera = world.spawn_actor(camera_bp, camera_init_trans, attach_to=ego_vehicle)

# Start camera with PyGame callback
camera.listen(lambda image: image.save_to_disk('out/%06d.png' % image.frame))

# Get gnss blueprint
gnss_bp = world.get_blueprint_library().find('sensor.other.gnss')
gnss = world.spawn_actor(gnss_bp, carla.Transform())

# Same result if I spawn a camera w/out attachment
# cam2 = world.spawn_actor(camera_bp, camera_init_trans)
# cam2.listen(lambda image: image.save_to_disk('out2/%06d.png' % image.frame))

time.sleep(2.0)

camera.destroy()
ego_vehicle.destroy()
gnss.destroy()
