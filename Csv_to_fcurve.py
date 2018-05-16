# Mission by Honeyclaw in IRC

import bpy
import csv


def slurp(fname):
    """ load all the data rows and return them in a list
    :param fname:
    :return:
    """
    rval = []
    with open(fname, 'r') as csvfile:
        r = csv.reader(csvfile, delimiter=' ')
        for row in r:
            rval.append(row)
    return rval

def make_or_get_fcurve(obj, data_path, index=-1):
    """
    :param obj: the data block from which we'll get the fcurve
    :param data_path:
    :param index:
    :return:
    """

    # freshly created objects don't have animation_data yet.
    if obj.animation_data is None:
        obj.animation_data_create()
    ad=obj.animation_data
    if ad.action is None:
        ad.action = bpy.data.actions.new(obj.name+"Action")

    for fc in ad.action.fcurves:
        if (fc.data_path != data_path):
            continue
        if index<0 or index==fc.array_index:
            return fc
    # the action didn't have the fcurve we needed, yet
    return ad.action.fcurves.new(data_path, index)

def set_keyframe(fcurve, time, val):
    kp = fcurve.keyframe_points

    for point in kp:
        if point.co[0] == time:
            point.co[1] = val
            point.interpolation = 'CONSTANT'
            return

    idx = len(kp)
    kp.add(1)
    kp[idx].co = (time, val)
    kp[idx].interpolation = 'CONSTANT'


def first_version():
    global rows, fcurves, event1, event2, row, t, i, kp, oldval, ec, newval, fr0
    # let's just jam a keyframe in there with its current value to simplify my life
    mat.keyframe_insert(data_path='diffuse_color', frame=1)
    fcurves = [
        None,
        make_or_get_fcurve(mat, 'diffuse_color', 0),
        make_or_get_fcurve(mat, 'diffuse_color', 1),
        make_or_get_fcurve(mat, 'diffuse_color', 2),
    ]
    # for event code 1, make it red
    event1 = [
        None, 1, 0, 0
    ]
    # for event code 2, make it green
    event2 = [
        None, 0, 1, 0
    ]
    for row in rows:
        t = float(row[0])
        for i in range(1, len(fcurves)):
            kp = fcurves[i].keyframe_points
            kp[len(kp) - 1].interpolation = 'CONSTANT'
            oldval = kp[len(kp) - 1].co[1]
            ec = int(row[1])
            if (ec == 1):
                newval = event1[i]
            elif (ec == 2):
                newval = event2[i]
            else:
                newval = 0
            fr0 = int(t * (fps))
            set_keyframe(fcurves[i], fr0, newval)
            set_keyframe(fcurves[i], fr0 + 10, oldval)


def do_event_1(mat, fr0):
    mat.diffuse_color=[1,0,0]
    mat.keyframe_insert(data_path='diffuse_color', frame=fr0)
    mat.diffuse_color=[0.8,0.8,0.8]
    mat.keyframe_insert(data_path='diffuse_color', frame=fr0+10)


def do_event_2(mat, fr0):
    mat.diffuse_color=[0,1,0]
    mat.keyframe_insert(data_path='diffuse_color', frame=fr0)
    mat.diffuse_color=[0.8,0.8,0.8]
    mat.keyframe_insert(data_path='diffuse_color', frame=fr0+15)


def second_version(rows, mat):
    mat.diffuse_color = [0.8,0.8,0.8]
    mat.keyframe_insert(data_path='diffuse_color', frame=1)
    for row in rows:
        t = float(row[0])
        fr0 = int(t*fps)
        ec = int(row[1])
        if ec==1:
            do_event_1(mat, fr0)
        elif ec==2:
            do_event_2(mat, fr0)
        else:
            raise "unknown event code %d"%ec

    for fc in mat.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = 'CONSTANT'

#


scn = bpy.context.scene
fps = scn.render.fps / scn.render.fps_base

obj = bpy.context.active_object

mat = obj.data.materials[0]

rows = slurp("/tmp/data.csv")

second_version(rows, mat)