#    Copyright 2023 ONERA - contact luis.bernardos@onera.fr
#
#    This file is part of MOLA.
#
#    MOLA is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MOLA is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with MOLA.  If not, see <http://www.gnu.org/licenses/>.

'''
Implements class **Zone**, which inherits from :py:class:`Node`

21/12/2021 - L. Bernardos - first creation
'''

import numpy as np
import re
from .. import misc as m
from .node import Node
from . import utils

# ref: https://github.com/CGNS/CGNS/blob/develop/src/cgnslib.h#L510
ELEMENTS_TYPES = [
    'Null', 'UserDefined',
    'NODE', 'BAR_2', 'BAR_3', 'TRI_3', 'TRI_6', 'QUAD_4', 'QUAD_8', 'QUAD_9',
    'TETRA_4', 'TETRA_10', 'PYRA_5', 'PYRA_14', 'PENTA_6', 'PENTA_15',
    'PENTA_18', 'HEXA_8', 'HEXA_20', 'HEXA_27', 'MIXED', 'PYRA_13',
    'NGON_n', 'NFACE_n', 'BAR_4', 'TRI_9', 'TRI_10', 'QUAD_12', 'QUAD_16',
    'TETRA_16', 'TETRA_20', 'PYRA_21', 'PYRA_29', 'PYRA_30', 'PENTA_24',
    'PENTA_38', 'PENTA_40', 'HEXA_32', 'HEXA_56', 'HEXA_64', 'BAR_5', 'TRI_12',
    'TRI_15', 'QUAD_P4_16', 'QUAD_25', 'TETRA_22', 'TETRA_34', 'TETRA_35',
    'PYRA_P4_29', 'PYRA_50', 'PYRA_55', 'PENTA_33', 'PENTA_66', 'PENTA_75',
    'HEXA_44', 'HEXA_98', 'HEXA_125']

class Zone(Node):
    """docstring for Zone"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setType('Zone_t')

        if self.value() is None:
            try:
                self.updateShape()
            except:
                self.setValue(np.array([[2,1,0]],dtype=np.int32,order='F'))


        if not self.childNamed('ZoneType'):
            Node(Name='ZoneType',Value='Structured',Type='ZoneType_t',Parent=self)

        if self.name() == 'Node': self.setName( 'Zone' )

    def save(self,*args,**kwargs):
        from .tree import Tree
        t = Tree(Base=self)
        t.save(*args,**kwargs)

    def isStructured(self):
        zone_type_node = self.get('ZoneType',Depth=1)
        if not zone_type_node:
            return False
        return zone_type_node.value() == 'Structured'
    
    def isUnstructured(self):
        zone_type_node = self.get('ZoneType',Depth=1)
        if not zone_type_node:
            return False
        return zone_type_node.value() == 'Unstructured'
    
    def getElementsTypes(self):
        types = set()
        elts_nodes = self.group(Type='Elements', Depth=1)

        if not elts_nodes:
            zone_type = self.get(Type='ZoneType', Depth=1).value()
            if zone_type == 'Structured':
                types.add('STRUCTURED')

        else:
            for elts in elts_nodes:
                enum = int(elts[1][0])
                types.add(ELEMENTS_TYPES[enum])
        return types

    def dim(self):
        if self.isStructured():
            try:
                return len(self.get('GridCoordinates',Depth=1).get('Coordinate*').value().shape)
            except:
                return self.value().shape[0]
        else:
            return self.value().shape[0]

    def shape(self):
        return self.get('GridCoordinates',Depth=1).get('Coordinate*').value().shape

    def numberOfPoints(self):
        return int(np.prod(self.value(), axis=0)[0])

    def numberOfCells(self):
        return int(np.prod(self.value(), axis=0)[1])

    def newFields(self, InputFields, Container='FlowSolution',
                  GridLocation='auto', dtype=np.float64, return_type='list',
                  ravel=False):

        if GridLocation == 'auto':
            GridLocation = m.AutoGridLocation[ Container ]

        FlowSolution = self.get(Container,Depth=1)
        if not FlowSolution:
            FlowSolution = Node(Parent=self, Name=Container, Type='FlowSolution_t',
                Children=[Node(Name='GridLocation', Type='GridLocation_t',
                               Value=GridLocation)])
        ExistingLocation = self.inferLocation( Container )
        if GridLocation != ExistingLocation:
            MSG = ('you requested GridLocation={} at {}, but existing fields'
                   ' are located at {}.\n'
                   'Please adapt Container or GridLocation values').format(
                                    GridLocation,Container,ExistingLocation)
            raise ValueError(m.RED+MSG+m.ENDC)

        if isinstance(InputFields,str):
            InputFields = {InputFields:0}
        elif isinstance(InputFields, list):
            InputFields = dict((key, 0) for key in InputFields)
        elif not isinstance(InputFields, dict):
            raise TypeError(f"attribute FieldNames must be a str, list or dict")

        arrays = []
        if GridLocation == 'Vertex':
            shape = self.value()[:,0]
        elif GridLocation == 'CellCenter':
            shape = self.value()[:,1]
        else:
            raise AttributeError('GridLocation=%s not supported'%GridLocation)

        for name, value in InputFields.items():
            array = np.full(shape, value, dtype=dtype, order='F')
            arrays += [ array ]
            Node(Parent=FlowSolution, Name=name, Type='DataArray_t', Value=array)
            if ravel: array = array.ravel(order='K')

        if return_type == 'list':
            if len(arrays) == 1: arrays = array
            return arrays
        elif return_type == 'dict':
            v = dict()
            for key, array in zip( list(InputFields), arrays):
                v[key] = array
            return v
        else:
            AttributeError('return_type=%s not supported'%return_type)

    
    def removeFields(self, FieldNames, Container='FlowSolution'):
        fs = self.get(Container, Depth=1)
        for field_name in FieldNames:
            field_node = fs.get(field_name,Depth=1)
            if field_node:
                field_node.remove()
            

    def fields(self, FieldNames, Container='FlowSolution',
             BehaviorIfNotFound='create', dtype=np.float64, return_type='list',
             ravel=False):
        if isinstance(FieldNames,str): FieldNames = [ FieldNames ]

        FlowSolution = self.childNamed( Container )

        if FlowSolution is None:
            if BehaviorIfNotFound == 'raise':
                raise ValueError('container %s not found in %s'%(Container,self.name()))
            elif BehaviorIfNotFound == 'create':
                return self.newFields(FieldNames, Container=Container,dtype=dtype)
            elif BehaviorIfNotFound == 'pass':
                return
            else:
                raise AttributeError(m.RED+'BehaviorIfNotFound=%s not supported'%BehaviorIfNotFound+m.ENDC)


        arrays = []
        for FieldName in FieldNames:
            FieldNode = FlowSolution.childNamed( FieldName )
            if FieldNode is None:
                if BehaviorIfNotFound == 'create':
                    array = self.newFields(FieldName,Container=Container,
                                           dtype=dtype, ravel=ravel)
                elif BehaviorIfNotFound == 'raise':
                    raise ValueError('%s not found in %s'%(FieldName,FlowSolution.path()))
                elif BehaviorIfNotFound == 'pass':
                    array = None

            else:
                array = FieldNode.value(ravel)

            arrays += [ array ]


        if return_type == 'list' or isinstance(return_type,list) or return_type is list:
            if len(arrays) == 1: return array
            return arrays
        elif return_type == 'dict' or isinstance(return_type,dict) or return_type is dict:
            v = dict()
            for key, array in zip( FieldNames, arrays):
                v[key] = array
            return v
        else:
            AttributeError('return_type=%s not supported'%return_type)

    def field(self, FieldName, **kwargs):
        if not isinstance(FieldName, str):
            raise AttributeError('FieldName must be of %s'%type(''))
        return self.fields( [FieldName], **kwargs )

    def xyz(self, Container='GridCoordinates', return_type='list',ravel=False):
        GC = self.get(Name='GridCoordinates', Depth=1)
        x = GC.get( Name='CoordinateX', Depth=1).value(ravel)
        y = GC.get( Name='CoordinateY', Depth=1).value(ravel)
        z = GC.get( Name='CoordinateZ', Depth=1).value(ravel)
        if return_type == 'list': return [x, y, z]
        else: return dict(CoordinateX=x, CoordinateY=y, CoordinateZ=z)

    def xy(self, Container='GridCoordinates', return_type='list',ravel=False):
        GC = self.get(Name='GridCoordinates', Depth=1)
        x = GC.get( Name='CoordinateX', Depth=1).value(ravel)
        y = GC.get( Name='CoordinateY', Depth=1).value(ravel)
        if return_type == 'list': return [x, y]
        else: return dict(CoordinateX=x, CoordinateY=y)

    def xz(self, Container='GridCoordinates', return_type='list',ravel=False):
        GC = self.get(Name='GridCoordinates', Depth=1)
        x = GC.get( Name='CoordinateX', Depth=1).value(ravel)
        z = GC.get( Name='CoordinateZ', Depth=1).value(ravel)
        if return_type == 'list': return [x, z]
        else: return dict(CoordinateX=x, CoordinateZ=z)

    def yz(self, Container='GridCoordinates', return_type='list',ravel=False):
        GC = self.get(Name='GridCoordinates', Depth=1)
        y = GC.get( Name='CoordinateY', Depth=1).value(ravel)
        z = GC.get( Name='CoordinateZ', Depth=1).value(ravel)
        if return_type == 'list': return [y, z]
        else: return dict(CoordinateY=y, CoordinateZ=z)

    def x(self, Container='GridCoordinates', return_type='list',ravel=False):
        GC = self.get(Name='GridCoordinates', Depth=1)
        x = GC.get( Name='CoordinateX', Depth=1).value(ravel)
        if return_type == 'list': return x
        else: return dict(CoordinateX=x)

    def y(self, Container='GridCoordinates', return_type='list',ravel=False):
        GC = self.get(Name='GridCoordinates', Depth=1)
        y = GC.get( Name='CoordinateY', Depth=1).value(ravel)
        if return_type == 'list': return y
        else: return dict(CoordinateY=y)

    def z(self, Container='GridCoordinates', return_type='list',ravel=False):
        GC = self.get(Name='GridCoordinates', Depth=1)
        z = GC.get( Name='CoordinateZ', Depth=1).value(ravel)
        if return_type == 'list': return z
        else: return dict(CoordinateZ=z)

    def allFields(self,include_coordinates=True,return_type='dict',ravel=False,
                  appendContainerToFieldName=False):

        if include_coordinates:
            arrays = self.xyz(ravel=ravel)
            FieldsNames = ['CoordinateX','CoordinateY','CoordinateZ']
        else:
            arrays = []
            FieldsNames = []
        AllFlowSolutionNodes = self.group(Type='FlowSolution_t',Depth=1)
        NbOfContainers = len(AllFlowSolutionNodes)
        if NbOfContainers > 1 and not appendContainerToFieldName and return_type=='dict':
            MSG = ('allFields(): several containers where detected, use'
                ' appendContainerToFieldName=True for avoid keyword overriding')
            print(m.YELLOW+MSG+m.ENDC)
        for FlowSolution in AllFlowSolutionNodes:
            for child in FlowSolution.children():
                if child.type() != 'DataArray_t': continue
                if appendContainerToFieldName:
                    FieldsNames += [ FlowSolution.name()+'/'+child.name() ]
                else:
                    FieldsNames += [ child.name() ]
                arrays += [ child.value(ravel=ravel) ]

        if return_type == 'dict':
            v = dict()
            for key, array in zip( FieldsNames, arrays ):
                v[key] = array
            return v
        elif return_type == 'list':
            return arrays
        else:
            AttributeError('return_type=%s not supported'%return_type)

    def assertFieldsSizeCoherency(self):
        for container in self.group(Type='FlowSolution_t'):
            data = container.group(Type='DataArray_t')
            if not data: continue
            
            all_data_have_same_size = all([d.value().size for d in data])
            if not all_data_have_same_size:
                raise ValueError(f"not all fields have same size at container {container.path()}")
            data_size = data[0].value().size

            grid_location_node = container.get('GridLocation')
            zone_npts = self.numberOfPoints()
            zone_ncells = self.numberOfCells()
            if grid_location_node:
                grid_location = grid_location_node.value()
                
                if grid_location == "Vertex":
                    if data_size != zone_npts:
                        raise ValueError((f'mismatch between zone nb of points ({zone_npts})'
                        f' and field size ({data_size}) at {container.path()}'))

                elif grid_location == "CellCenter":
                    if data_size != zone_ncells:
                        raise ValueError((f'mismatch between zone nb of cells ({zone_ncells})'
                        f' and field size ({data_size}) at {container.path()}'))

                else: 
                    raise ValueError(f'unsupported GridLocation "{grid_location}"')

            else:
                if data_size not in (zone_npts, zone_ncells):
                    raise ValueError((f'data size ({data_size}) does not correspond'
                        f' to neither zone npts ({zone_npts}) nor ncells ({zone_ncells})'))


    def inferLocation(self, Container ):
        if Container == 'GridCoordinates': return 'Vertex'
        FlowSolution = self.get( Name=Container )
        if not FlowSolution:
            MSG = 'Container %s not found in %s'%(Container,self.path())
            raise ValueError(m.RED+MSG+m.ENDC)
        try:
            return FlowSolution.get( Name='GridLocation' ).value()
        except:
            if not FlowSolution.children(): return m.AutoGridLocation[ Container ]

            FieldSize = self._size_of_data_array_in_container(FlowSolution)
            if FieldSize == self.numberOfPoints(): return 'Vertex'
            elif FieldSize == self.numberOfCells(): return 'CellCenter'
            else:
                raise ValueError((f'new field size ({FieldSize}) did not match zone'
                f' npts ({self.numberOfPoints()}) nor ncells ({self.numberOfCells()})'
                f' at container {FlowSolution.path()}'))

    @staticmethod
    def _size_of_data_array_in_container(flow_solution_node):
        child = flow_solution_node.get(Type="DataArray_t")
        if not child: return 0
        return child.value().size


    def useEquation(self, equation, Container='FlowSolution', ravel=False):
        RegExpr = r"{[^}]*}"
        eqnVarsWithDelimiters = re.findall( RegExpr, equation )
        adaptedEqnVars = []

        v = self.allFields(ravel=ravel,appendContainerToFieldName=False)

        adaptedEqnVars, AllContainers = [], []
        for i, eqnVarWithDelimiters in enumerate(eqnVarsWithDelimiters):
            eqnVar = eqnVarWithDelimiters[1:-1]
            if eqnVar in ['CoordinateX','CoordinateY','CoordinateZ']:
                AllContainers.append( 'GridCoordinates' )
                adaptedEqnVars.append( "v['%s']"%eqnVar)

            elif len(eqnVar) == 1 and eqnVar.lower() in ['x','y','z']:
                AllContainers.append( 'GridCoordinates' )
                adaptedEqnVars.append( "v['Coordinate%s']"%eqnVar.upper() )

            else:
                eqnVarSplit = eqnVar.split('/')
                if len(eqnVarSplit) == 1:
                    eqnContainer = Container
                    eqnVarName = eqnVar
                else:
                    eqnContainer = eqnVarSplit[0]
                    eqnVarName = eqnVarSplit[1]

                eqnContainerAndName = eqnContainer+'/'+eqnVarName
                if eqnContainerAndName not in v:
                    if i ==0:
                        field = self.fields(eqnVarName, Container=eqnContainer,
                                    ravel=ravel, return_type='list')
                    else:
                        raise ValueError('unexpected')

                    v[eqnContainerAndName] = field
                AllContainers.append( eqnContainer )
                adaptedEqnVars.append( "v['%s']"%eqnContainerAndName )
        FirstMemberLocation = self.inferLocation(AllContainers[0])
        SecondMemberLocations = [self.inferLocation(c) for c in AllContainers[1:]]
        mixedLocations = False
        for i, SecondMemberLocation in enumerate(SecondMemberLocations):
            if FirstMemberLocation != SecondMemberLocation:
                mixedLocations = True
                break


        adaptedEqnVars[0] += '[:]'

        adaptedEquation = equation
        for keyword, adapted in zip(eqnVarsWithDelimiters, adaptedEqnVars):
            adaptedEquation = adaptedEquation.replace(keyword, adapted)

        try:
            exec(adaptedEquation,globals(),{'v':v,'np':np})
        except BaseException as e:
            print(m.RED+'ERROR : could not apply equation:\n'+adaptedEquation+m.ENDC)
            if mixedLocations:
                print(m.RED+'This may be due to mixing values located in both Vertex and CellCenter'+m.ENDC)
            raise e

    def hasFields(self):
        return bool( self.get( Type='FlowSolution_t', Depth=1 ) )

    def boundaries(self):
        if not self.isStructured(): 
            raise ValueError('boundaries only implemented for structured zones')
        
        dim = self.dim()
        if dim == 3:
            bnds = [self.imin(), self.imax(),
                    self.jmin(), self.jmax(),
                    self.kmin(), self.kmax()]
        elif dim == 2:
            bnds = [self.imin(), self.imax(),
                    self.jmin(), self.jmax()]
        else:
            bnds = [self.imin(), self.imax()]
        
        return bnds


    def boundary(self, index='i', bound='min'):
        if not self.isStructured(): 
            raise ValueError(f'boundary only meaningful for structured zone')

        x, y, z, containers, fieldnames, fields = self._xyz_containers_fieldsnames_fields()

        if bound == 'min':
            bnd = 0
        elif bound == 'max':
            bnd = -1
        else:
            raise ValueError(f'bound {bound} not implemented. Must be "min" or "max"')

        if index == 'i':
            if self.dim() == 3:
                x = x[bnd,:,:]
                y = y[bnd,:,:]
                z = z[bnd,:,:]
                for i, f in enumerate(fields[:]):
                    fields[i] = f[bnd,:,:]
            elif self.dim() == 2:
                x = x[bnd,:]
                y = y[bnd,:]
                z = z[bnd,:]
                for i, f in enumerate(fields[:]):
                    fields[i] = f[bnd,:]
            else:
                x = np.atleast_1d(x[bnd])
                y = np.atleast_1d(y[bnd])
                z = np.atleast_1d(z[bnd])
                for i, f in enumerate(fields[:]):
                    fields[i] = np.atleast_1d(f[bnd])

        elif index == 'j':
            if self.dim() == 3:
                x = x[:,bnd,:]
                y = y[:,bnd,:]
                z = z[:,bnd,:]
                for i, f in enumerate(fields[:]):
                    fields[i] = f[:,bnd,:]
            elif self.dim() == 2:
                x = x[:,bnd]
                y = y[:,bnd]
                z = z[:,bnd]
                for i, f in enumerate(fields[:]):
                    fields[i] = f[:,bnd]
            else:
                raise ValueError(f'cannot extract {index+bound} from 1D zone')

        elif index == 'k':
            if self.dim() == 3:
                x = x[:,:,bnd]
                y = y[:,:,bnd]
                z = z[:,:,bnd]
                for i, f in enumerate(fields[:]):
                    fields[i] = f[:,:,bnd]
            else:
                raise ValueError(f'cannot extract {index+bound} from f{self.dim()}D zone')

        x_orderF = np.copy(x,order='F')
        y_orderF = np.copy(y,order='F')
        z_orderF = np.copy(z,order='F')

        zone = utils.newZoneFromArrays(self.name()+f'_{index+bound}',
                    ['x','y','z'], [x_orderF,y_orderF,z_orderF])
        contDict = dict()
        if len(containers) == 0: return zone

        for container, fieldname, field in zip(containers, fieldnames, fields):
            try:
                contDict[container][fieldname] = np.copy(field,order='F') 
            except KeyError:
                contDict[container] = {fieldname:np.copy(field,order='F')}

        for container, fieldname in contDict.items():
            zone.setParameters(container, ContainerType='FlowSolution_t',
                **contDict[container])

        return zone


    def imin(self): return self.boundary('i','min')

    def imax(self): return self.boundary('i','max')

    def jmin(self): return self.boundary('j','min')

    def jmax(self): return self.boundary('j','max')

    def kmin(self): return self.boundary('k','min')

    def kmax(self): return self.boundary('k','max')


    def _xyz_containers_fieldsnames_fields(self):
        x,y,z = self.xyz()
        allfields = self.allFields(include_coordinates=False,
                                appendContainerToFieldName=True)
        containers, fieldnames, fields = [], [], []
        for name, field in allfields.items():
            container, fieldname = name.split('/')
            containers += [container]
            fieldnames += [fieldname]
            fields += [field]

        return x, y, z, containers, fieldnames, fields
    
    def getArrayShapes(self):
        shape_vertex = None
        shape_cellcenter = None

        def get_containers_at_vertex():
            containers = self.group(Type='GridCoordinates', Depth=1)
            for fs in self.group(Type='FlowSolution', Depth=1):
                GridLocation = fs.get(Type='GridLocation')
                if GridLocation is None or GridLocation == 'Vertex':
                    containers.append(fs)
            return containers

        def get_containers_at_cellcenter():
            containers = []
            for fs in self.group(Type='FlowSolution', Depth=1):
                GridLocation = fs.get(Type='GridLocation')
                if GridLocation is not None and GridLocation == 'CellCenter':
                    containers.append(fs)
            return containers

        for container in get_containers_at_vertex():
            for node in container.group(Type='DataArray'):
                shape = node.value().shape
                if shape_vertex is None:
                    shape_vertex = shape
                else:
                    assert shape == shape_vertex, f'{node.Path} has a different shape ({shape}) that others located at Vertex ({shape_vertex})'

        for container in get_containers_at_cellcenter():
            for node in container.group(Type='DataArray'):
                shape = node.value().shape
                if shape_cellcenter is None:
                    shape_cellcenter = shape
                else:
                    assert shape == shape_cellcenter, f'{node.Path} has a different shape ({shape}) that others located at CellCenter ({shape_cellcenter})'

        assert shape_vertex is not None or shape_cellcenter is not None, 'Cannot use this method on a Zone without DataArray nodes'
        if shape_cellcenter is None:
            shape_cellcenter = tuple(np.array(shape_vertex) - 1)
        elif shape_vertex is None:
            shape_vertex = tuple(np.array(shape_cellcenter) + 1)

        return shape_vertex, shape_cellcenter
    
    def updateShape(self):
        shape_vertex, _ = self.getArrayShapes()
        if isinstance(shape_vertex, int):
            shape_vertex = (shape_vertex,)

        value = np.array([[v, v - 1, 0] for v in shape_vertex], dtype=np.int32, order='F')
        self.setValue(value)

