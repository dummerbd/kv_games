from kivy.factory import Factory
from kivy.properties import (
    ObjectProperty, NumericProperty, ListProperty, BooleanProperty,
    StringProperty)

from kivent_core.systems.staticmemgamesystem cimport (
    StaticMemGameSystem, MemComponent)
from kivent_core.memory_handlers.zone cimport MemoryZone
from kivent_core.systems.position_systems cimport PositionStruct2D


cdef class VelocityComponent2D(MemComponent):

    property entity_id:
        def __get__(self):
            cdef VelocityStruct2D* data = <VelocityStruct2D*>self.pointer
            return data.entity_id

    property vx:
        def __get__(self):
            cdef VelocityStruct2D* data = <VelocityStruct2D*>self.pointer
            return data.vx
        def __set__(self, float value):
            cdef VelocityStruct2D* data = <VelocityStruct2D*>self.pointer
            data.vx = value

    property vy:
        def __get__(self):
            cdef VelocityStruct2D* data = <VelocityStruct2D*>self.pointer
            return data.vy
        def __set__(self, float value):
            cdef VelocityStruct2D* data = <VelocityStruct2D*>self.pointer
            data.vy = value

    property vel:
        def __get__(self):
            cdef VelocityStruct2D* data = <VelocityStruct2D*>self.pointer
            return (data.vx, data.vy)
        def __set__(self, tuple new_vel):
            cdef VelocityStruct2D* data = <VelocityStruct2D*>self.pointer
            data.vx = new_vel[0]
            data.vy = new_vel[1]

    property bounds_x0:
        def __get__(self):
            cdef VelocityStruct2D* data = <VelocityStruct2D*>self.pointer
            return data.bounds_x0
        def __set__(self, int value):
            cdef VelocityStruct2D* data = <VelocityStruct2D*>self.pointer
            data.bounds_x0 = value

    property bounds_y0:
        def __get__(self):
            cdef VelocityStruct2D* data = <VelocityStruct2D*>self.pointer
            return data.bounds_y0
        def __set__(self, int value):
            cdef VelocityStruct2D* data = <VelocityStruct2D*>self.pointer
            data.bounds_y0 = value

    property bounds_x1:
        def __get__(self):
            cdef VelocityStruct2D* data = <VelocityStruct2D*>self.pointer
            return data.bounds_x1
        def __set__(self, int value):
            cdef VelocityStruct2D* data = <VelocityStruct2D*>self.pointer
            data.bounds_x1 = value

    property bounds_y1:
        def __get__(self):
            cdef VelocityStruct2D* data = <VelocityStruct2D*>self.pointer
            return data.bounds_y1
        def __set__(self, int value):
            cdef VelocityStruct2D* data = <VelocityStruct2D*>self.pointer
            data.bounds_y1 = value


cdef class VelocitySystem2D(StaticMemGameSystem):
    system_id = StringProperty('velocity')
    processor = BooleanProperty(True)
    type_size = NumericProperty(sizeof(VelocityStruct2D))
    component_type = ObjectProperty(VelocityComponent2D)
    system_names = ListProperty(['velocity', 'position'])

    def init_component(self, unsigned int component_index, unsigned int entity_id, str zone, args):
        cdef float vx = args[0][0]
        cdef float vy = args[0][1]
        cdef int bounds_x0 = args[1][0]
        cdef int bounds_y0 = args[1][1]
        cdef int bounds_x1 = args[1][2]
        cdef int bounds_y1 = args[1][3]
        cdef MemoryZone memory_zone = self.imz_components.memory_zone
        cdef VelocityStruct2D* comp_ptr = <VelocityStruct2D*>(
            memory_zone.get_pointer(component_index))
        comp_ptr.entity_id = entity_id
        comp_ptr.vx = vx
        comp_ptr.vy = vy
        comp_ptr.bounds_x0 = bounds_x0
        comp_ptr.bounds_y0 = bounds_y0
        comp_ptr.bounds_x1 = bounds_x1
        comp_ptr.bounds_y1 = bounds_y1
        return self.entity_components.add_entity(entity_id, zone)

    def clear_component(self, unsigned int component_index):
        cdef MemoryZone memory_zone = self.imz_components.memory_zone
        cdef VelocityStruct2D* comp_ptr = <VelocityStruct2D*>(
            memory_zone.get_pointer(component_index))
        comp_ptr.entity_id = -1

    def remove_component(self, unsigned int component_index):
        cdef VelocityComponent2D comp = self.components[component_index]
        self.entity_components.remove_entity(comp.entity_id)
        super().remove_component(component_index)

    def update(self, dt):
        gameworld = self.gameworld
        cdef void** comp_data = <void**>(self.entity_components.memory_block.data)
        cdef unsigned int comp_count = self.entity_components.count
        cdef unsigned int count = self.entity_components.memory_block.count
        cdef unsigned int i, real_index
        cdef PositionStruct2D* comp_pos
        cdef VelocityStruct2D* comp_vel

        for i in range(count):
            real_index = i * comp_count
            if comp_data[real_index] == NULL:
                continue
            comp_vel = <VelocityStruct2D*>comp_data[real_index]
            comp_pos = <PositionStruct2D*>comp_data[real_index + 1]
            comp_pos.x += comp_vel.vx * dt
            comp_pos.y += comp_vel.vy * dt
            if comp_pos.x <= comp_vel.bounds_x0:
                comp_pos.x = comp_vel.bounds_x1
            elif comp_pos.x >= comp_vel.bounds_x1:
                comp_pos.x = comp_vel.bounds_x0
            if comp_pos.y <= comp_vel.bounds_y0:
                comp_pos.y = comp_vel.bounds_y1
            elif comp_pos.y >= comp_vel.bounds_y1:
                comp_pos.y = comp_vel.bounds_y0


Factory.register('VelocitySystem2D', cls=VelocitySystem2D)
