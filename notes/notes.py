import datetime
from flask import Blueprint
from flask import request, g, jsonify
from . import db

bp = Blueprint("notes", "notes", url_prefix="/notes")


@bp.route("/addnew", methods=["GET","POST"])
def addnote():
    conn = db.get_db()
    cursor = conn.cursor()

    cursor.execute("select tagname from hashtags")
    tags=(x[0] for x in cursor.fetchall())
    mark={}

    title = request.json["title"]
    detail = request.json["detail"]
    for t in tags:
        mark[t]=request.json[f"{t}"]
    created_on = datetime.datetime.now()

    cursor.execute("insert into notes (title,created_on, detail)values (%s, %s, %s)", (title, created_on,detail,))
    
    cursor.execute("select tagname from hashtags")
    tags=(x[0] for x in cursor.fetchall())
    
    for t in tags:
        if mark[t]:
            cursor.execute("""insert into tags_notes (note, tag) values ((select id from notes where detail=%s),
            (select id from hashtags where tagname=%s))""",(detail,t,))
    conn.commit()
    return "ok",200


@bp.route("/")
def allnotes():
    conn = db.get_db()
    cursor = conn.cursor()

    cursor.execute(
            "select tagname from hashtags"
        )
    tags=(x[0] for x in cursor.fetchall())
    tags=list(tags)

    cursor.execute(
        "select id, title, created_on from notes order by created_on desc"
    )
    notes = cursor.fetchall()

    return jsonify(dict(notes=[dict(id=id, title=title, created_on=created_on.strftime("%c")) for id, title, created_on in notes]))


@bp.route("/<nid>")
def notedetail(nid):
    conn = db.get_db()
    cursor = conn.cursor()

    cursor.execute(
        "select title, created_on, detail from notes where id=%s", (nid,)
    )
    note = cursor.fetchone()

    cursor.execute(
        "select t.tagname from hashtags t, tags_notes tn where t.id=tn.tag and tn.note=%s",(nid,)
        )
    tags=(x[0] for x in cursor.fetchall())
    tags=list(tags)

    title, created_on, detail = note
    nid = int(nid)

    ret = dict(
        id=nid,
        detail=detail,
        title=title,
        created_on=created_on.strftime("%c"),
        tags=tags
    )
    return jsonify(dict(note=ret))



@bp.route("/<nid>/edit", methods=[ "POST", ])
def editnote(nid):
    conn=db.get_db()
    cursor=conn.cursor()

    cursor.execute(
        "select t.tagname from hashtags t, tags_notes tn where t.id=tn.tag and tn.note=%s",(nid,)
        )
    tags=(x[0] for x in cursor.fetchall())
    tags=list(tags)

    cursor.execute(
        "select tagname from hashtags"
    )
    alltags=(x[0] for x in cursor.fetchall())
    alltags=list(alltags)

    title=request.json["title"]
    detail=request.json["detail"]

    for t in alltags:
        if request.json[f"{t}"]:
            if t not in tags:
                cursor.execute(
                    "insert into tags_notes(note,tag)values (%s,(select id from hashtags where tagname=%s))",(nid,t,)
                )
        else:
            if t in tags:
                cursor.execute(
                    "delete from tags_notes where note=%s and tag=(select id from hashtags where tagname=%s)",(nid,t,)
                )

    cursor.execute(
        "update notes set title=%s, detail=%s where id=%s",(title,detail,nid)
        )
    conn.commit()
    
    cursor.execute(
        "select title, created_on, detail from notes where id=%s", (nid,)
        )
    note = cursor.fetchone()

    cursor.execute(
        "select t.tagname from hashtags t, tags_notes tn where t.id=tn.tag and tn.note=%s",(nid,)
        )

    tags=(x[0] for x in cursor.fetchall())
    tags=list(tags)

    title, created_on, detail = note
    nid = int(nid)

    ret = dict(
            id=nid,
            detail=detail,
            title=title,
            created_on=created_on.strftime("%c"),
            tags=tags
        )
    return jsonify(dict(note=ret))


@bp.route("/deletenote/<nid>", methods=["DELETE",])
def deletenote(nid):
    conn=db.get_db()
    cursor=conn.cursor()

    cursor.execute(
        "delete from tags_notes where note=%s", (nid,)
    )

    cursor.execute(
        "delete from notes where id=%s",(nid,)
    )

    conn.commit()
    return "ok",200 
    


@bp.route("/newtag",methods=["GET","POST"])
def newtag():
    conn = db.get_db()
    cursor = conn.cursor() 

    newtag=request.json["newtag"]
    cursor.execute("insert into hashtags (tagname) values (%s)",(newtag,))

    conn.commit()
    return "ok",200
        

@bp.route("/search",methods=["POST",])
def search():
    conn = db.get_db()
    cursor = conn.cursor()
 
    searchstring=request.json["searchstring"]
    tag=request.json["tag"]
   
    if searchstring and tag:
        searchstring='%'+searchstring+'%'
       
        cursor.execute(
            "select n.id, n.title, n.created_on from notes n, hashtags t, tags_notes tn where n.id=tn.note and t.tagname=%s and t.id=tn.tag and (title ilike  %s or detail ilike %s)",(tag,searchstring,searchstring,)
        )

    elif searchstring:
        searchstring='%'+searchstring+'%'
        
        cursor.execute(
            "select id, title, created_on from notes where title ilike %s or detail ilike %s",(searchstring,searchstring,)
        )

    elif tag:
     
        cursor.execute(
            "select n.id, n.title, n.created_on from notes n, hashtags t, tags_notes tn where t.tagname=%s and n.id=tn.note and tn.tag=t.id",(tag,)
        )
        
    notes=cursor.fetchall()

    return jsonify(dict(notes=[dict(id=id, title=title, created_on=created_on) for id, title, created_on in notes]))
 
