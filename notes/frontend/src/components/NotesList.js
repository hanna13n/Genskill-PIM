import React from 'react'

function NotesList(props){
    const noteDetail = (e,note) => {
        e.preventDefault()
        props.noteDetail(note.id)
    }


    return(
        
        <ol>
        
            {props.notes && props.notes.notes.map(note => {
                        return (
                            
                            <li key={note.id}>
                            <hr/>
                            <a href="/notes/" onClick= {(e) => noteDetail(e,note)}>
                                <div className="row">
                                <div className="col-lg-6">
                                <h6>{note.title}</h6>
                                </div>
                                <div className="col-lg-6">
                                <small>{note.created_on}</small>
                                </div>
                                </div>
                                </a>
                               
                            </li>
                            
                        )
                    })
                    
            }
                   
        </ol>
        
    )
}

export default NotesList