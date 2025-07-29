# === Graph Exceptions

class NodeAlreadyInGraph(Exception):
    def __init__(self, node):
        self.message    = 'Node is already added into graph:'
        self.node       = node

        super(NodeAlreadyInGraph, self).__init__( (self.message, node) )

    def __reduce__(self):
        return (NodeAlreadyInGraph, (self.message, self.node))


class SourceNodeNotInGraph(Exception):
    def __init__(self, node):
        self.message    = 'Source node is not in graph:'
        self.node       = node

        super(SourceNodeNotInGraph, self).__init__( (self.message, node) )

    def __reduce__(self):
        return (SourceNodeNotInGraph, (self.message, self.node))


class TargetNodeNotInGraph(Exception):
    def __init__(self, node):
        self.message    = 'Target node is not in graph:'
        self.node       = node

        super(TargetNodeNotInGraph, self).__init__( (self.message, node) )

    def __reduce__(self):
        return (TargetNodeNotInGraph, (self.message, self.node))


class StartNodeAlreadyExists(Exception):
    def __init__(self, node):
        self.message    = 'Start node is already added into graph:'
        self.node       = node

        super(StartNodeAlreadyExists, self).__init__( (self.message, node) )

    def __reduce__(self):
        return (StartNodeAlreadyExists, (self.message, self.node))


class EndNodeAlreadyExists(Exception):
    def __init__(self, node):
        self.message    = 'End node is already added into graph:'
        self.node       = node

        super(EndNodeAlreadyExists, self).__init__( (self.message, node) )

    def __reduce__(self):
        return (EndNodeAlreadyExists, (self.message, self.node))


# === Loader Exceptions

class UnknownFormType(Exception):
    def __init__(self, f_type):
        self.message    = 'Unknown form type:'
        self.f_type     = f_type

        super(UnknownFormType, self).__init__( (self.message, f_type) )

    def __reduce__(self):
        return (UnknownFormType, (self.message, self.f_type))


class UnknownFormType(Exception):
    def __init__(self, f_type):
        self.message    = 'Unknown form type:'
        self.f_type     = f_type

        super(UnknownFormType, self).__init__( (self.message, f_type) )

    def __reduce__(self):
        return (UnknownFormType, (self.message, self.f_type))


class TableIsEmpty(Exception):
    def __init__(self, table):
        self.message    = 'Table is empty:'
        self.table      = table

        super(TableIsEmpty, self).__init__( (self.message, table) )

    def __reduce__(self):
        return (TableIsEmpty, (self.message, self.table))

