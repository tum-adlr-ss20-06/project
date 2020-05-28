import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage


def random_workspace(grid_size, num_obj_max, obj_size_avg):
    """generates a workspace of size: grid_size x grid_size with obstacles indicated with ones.
        Free space are indicated with a 0. 
        The # of objects, the origin and height & width of the objects are generated from uniform and normal distributions.
    """  
    #Throw number of objects from a uniform distribution.
    num_objects= np.random.randint(low=1, high=num_obj_max, size=None)
    #num_objects = tf.random.uniform(shape=[], minval=0, maxval=num_obj_max, dtype=tf.int32, seed=None, name=None)

    #Generate an origin from a uniform distribution for each object
    origin= np.random.randint(low=0, high=grid_size, size=(num_objects,2))
    origin=np.asarray(origin, dtype=None, order=None)
    #origin = tf.random.uniform( 
    #shape=[num_objects,2], minval=0, maxval=grid_size, dtype=tf.int32, seed=None, name=None)

    #Generate a width and height from a Gaussian distribution for each object
    width =np.random.normal(loc=obj_size_avg, scale=2, size=(num_objects,1))
    width=np.asarray(width, dtype=int, order=None)
    #width = tf.random.normal(shape=[num_objects,1], mean=obj_size_avg, stddev=2, dtype=tf.int32)

    height =np.random.normal(loc=obj_size_avg, scale=2, size=(num_objects,1))
    height =np.asarray(height, dtype=int, order=None)
    #height = tf.random.normal(shape=[num_objects,1], mean=obj_size_avg, stddev=2, dtype=tf.int32)

    #Initialize workspace
    workspace=np.zeros((grid_size,grid_size), dtype=int)

    #Assign each entry with an object a 1. 
    for i in range(num_objects):
        if origin[i,1]+width[i] > grid_size:
            right_bound=grid_size+1
        else: right_bound = (origin[i,1]+width[i]).item()

        if origin[i,0]+height[i] > grid_size:
            upper_bound=grid_size+1
        else: upper_bound = (origin[i,0]+height[i]).item()
        workspace[origin[i,0]:upper_bound, origin[i,1]:right_bound]=1
        workspace

    return workspace


def get_start_goal_for_workspace(workspace):
    """generates a start and goal point for a given workspace. 
    It throws in randomply points until the points are in free space.
    """

    grid_size = workspace.shape[0]

    #Generate start point (repeat until point is found where no object ist placed)
    start_blocked = 1
    while (start_blocked == 1):
        start = np.random.randint(low=0, high=grid_size, size=(1,2))
        start = np.asarray(start, dtype=None, order=None)
        y = start[0,0]
        x = start[0,1]
        start_blocked = workspace[y, x]
        #start = tf.random.uniform( 
        #shape=[1,2], minval=0, maxval=grid_size, dtype=tf.int32, seed=None, name=None)

    #Generate goal point (repeat until point is found where no object ist placed) and assign goal point with a 1
    goal_blocked = 1
    while (goal_blocked == 1):
        goal = np.random.randint(low=0, high=grid_size, size=(1,2))
        goal = np.asarray(goal, dtype=None, order=None)
        y = goal[0,0]
        x = goal[0,1]
        goal_blocked = workspace[y, x]
        #goal = tf.random.uniform( 
        #shape=[1,2], minval=0, maxval=grid_size, dtype=tf.int32, seed=None, name=None)

    return start, goal


def visualize_workspace(workspace, fignum=1):
    """for nicely visualizing a workspace."""

    fig = plt.figure(fignum)
    ax = fig.add_subplot(221)
    cax = ax.matshow(workspace)
    fig.colorbar(cax)

    return fig

def visualize_distance_field(workspace, fignum=1):
    """for nicely visualizing the distance field to the obstacles."""
    dist_img = ndimage.distance_transform_edt(-workspace + 1)  # Excpects blocks as 0 and free space as 1
    
    fig = plt.figure(fignum)
    
    dm = fig.add_subplot(222)
    cdm=dm.imshow(dist_img, cmap='Reds')
    cdm=dm.imshow(workspace, cmap='Blues', alpha=0.3)
    
    return fig

def image_interpolation(*, img, pixel_size=1, order=1, mode='nearest'):

    factor = 1 / pixel_size

    def interp_fun(x):
        x2 = x.copy()

        if x2.ndim == 1:
            x2 = x2[np.newaxis, :]
        # Transform physical coordinates to image coordinates 
        x2 *= factor
        x2 -= 0.5

        return ndimage.map_coordinates(input=img, coordinates=x2.T, order=order, mode=mode).T

    return interp_fun

    
############# TEST SAMPLE WORKSPACE #########################

if __name__ == '__main__':
    workspace_sample = random_workspace(32, 10, 5)
    start, goal = get_start_goal_for_workspace(workspace_sample)

    workspace_sample[start[0, 0], start[0, 1]] = 2
    workspace_sample[goal[0, 0], goal[0, 1]] = 3

    fig1 = visualize_workspace(workspace_sample)
    fig2= visualize_distance_field(workspace_sample)
    plt.show()

    
    #Calculates the distance from a point "x" to the nearest obstacle
    pixel_size=1 #10/32
    dist_img = ndimage.distance_transform_edt(-workspace_sample + 1)  # Excpects blocks as 0 and free space as 1
    dist_fun = image_interpolation(img=dist_img, pixel_size=pixel_size)
    x=np.array([float(start[0,0]),float(start[0,1])])
    dist= dist_fun(x=x)
    
    print("Distance to the nearest obstacle at the center: ",
       dist )