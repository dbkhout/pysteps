import numpy as np

"""The forecast methods in the nowcasts module implement the following interface:

    forecast(R, V, num_timesteps, non-keyworded arguments, keyword arguments)

where R (m,n) is the input precipitation field to be extrapolated and V (2,m,n) is
an array containing  the x- and y-components of the m*n advection field. num_timesteps
is an integer specifying the number of time steps to forecast.
Non-keyworded arguments specific to each method can be included 
The interface accepts additional ptional keyword arguments that are specific to a given 
forecast method.
        
The output of each method is a three-dimensional array of shape (num_timesteps,m,n) 
containing a time series of nowcast precipitation fields.

"""

def get_method(name):
    """Return one callable function to produce deterministic or ensemble 
    precipitation nowcasts.\n\
    
    Methods for precipitation nowcasting:
    +-------------------+-------------------------------------------------------+
    |     Name          |              Description                              |
    +===================+=======================================================+
    |  eulerian         | this approach simply keeps the last observation       |
    |                   | frozen (Eulerian persistence)                         |
    +-------------------+-------------------------------------------------------+
    |  lagrangian or    | this approach extrapolate the last observation        |
    |  extrapolation    | following the motion field (Lagrangian persistence)   |
    +-------------------+-------------------------------------------------------+
    |                   | implementation of the STEPS stochastic nowcasting     |
    |  steps            | method as described in Seed (2003), Bowler et al      |
    |                   | (2006) and Seed et al (2013)                          |
    +-------------------+-------------------------------------------------------+

    """
    if name.lower() in ["eulerian"]:
        def eulerian(R, V, num_timesteps, *args, **kwargs):
            return np.repeat(R[None, :, :,], num_timesteps, axis=0)
        return eulerian
    elif name.lower() in ["extrapolation", "lagrangian"]:
        from . import simple_advection
        return simple_advection.forecast
    elif name.lower() in ["steps"]:
        from . import steps
        return steps.forecast
    else:
        raise ValueError("unknown nowcasting method %s" % name)
