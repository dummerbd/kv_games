from kivent_core.systems.staticmemgamesystem cimport (
    StaticMemGameSystem, 
    MemComponent)


ctypedef struct VelocityStruct2D:
    unsigned int entity_id
    float vx
    float vy
    int bounds_x0
    int bounds_y0
    int bounds_x1
    int bounds_y1


cdef class VelocityComponent2D(MemComponent):
    pass


cdef class VelocitySystem2D(StaticMemGameSystem):
    pass
