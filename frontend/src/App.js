import {useState, useEffect} from 'react'
import './App.css';
import NotesList from './components/NotesList';
import NoteDetail from './components/NoteDetail';
import EditNote from './components/EditNote';
import AddNote from './components/AddNote';
import AddTag from './components/AddTag';

function App() {

  const[page, setPage] = useState("home")
  const[notes, setNotes] = useState()
  const [tags, setTags]=useState()
  const [Detail, setDetail] = useState()
  const [editedNote, setEditedNote] =useState()
  const[loadNote, setLoadNotes]=useState(false)
  const[searchTag, setSearchTag]=useState(null)
  const[search, setSearch]=useState(null)
  const[loadTag, setLoadTags]=useState(false)

  useEffect(() => {
    fetch(process.env.REACT_APP_API_SERVER+"/notes/",
    {
      method: 'GET',
      headers: { 'Accept' : 'application/json',
      'Content-type': 'application/json',
     }})
     .then(resp => resp.json())
    .then((resp) => setNotes(resp))
    .catch(error => console.log(error)) 
  },[loadNote])

  useEffect(()=>{
    fetch(process.env.REACT_APP_API_SERVER+"/",
      { 
        method: 'GET',
        headers: { 'Accept': 'application/json',
        'Content-type': 'application/json',
       } })
       .then(resp => resp.json())
      .then((resp) => setTags(resp))
      .catch(error => console.log(error))
      },[loadTag])
  
  const noteDetail = (id) => {
      setDetail(id)
      setPage("detail")
  }
    
  

  const editNote = (note) =>{
    setEditedNote(note)
    setPage("editform")
  
  }


  const Success= (field,id) =>
  {
    if(field==="note")
      {
        setLoadNotes(!loadNote)
        if(id)
         noteDetail(id)
        else
          setPage("home")
      }

    else
      {
        setLoadTags(!loadTag)
        setPage("home")
      }
  }

  function searchNote(e){
    e.preventDefault()
    var body={}
    body["searchstring"]=search
    body["tag"]=searchTag

    fetch(
      process.env.REACT_APP_API_SERVER+"/notes/search", 
      {
          method: 'POST',
          headers: { 'Accept' : 'application/json',
          'Content-type': 'application/json',
       },
       body:JSON.stringify(body),
      }
   ).then(resp => resp.json())
   .then(resp => setNotes(resp))
   .catch(err => console.log(err))

    setPage("searchresults")

  }
  

  return (

    <div className="App">


      <nav className="navbar sticky-top nav-bar-dark navbar-expand-lg">
        <div className="container-fluid">
          <a className="navbar-brand link" href="/"><h1>EasyNote</h1></a>

          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"><h1><i class="bi bi-justify"></i></h1></span>
          </button>

          <div className="collapse navbar-collapse" id="navbarTogglerDemo02">

          <ul className="navbar-nav ms-auto mb-2 mb-lg-0">

            <li className="nav-item">
              <button className="nav-link btn btn-link link"   onClick={() => setPage("addnoteform")} > + Add Note </button>
            </li>

            <li className="nav-item">
              <button className="nav-link btn btn-link link" onClick={() => setPage("addtagform")}> + Add Tag </button>
            </li>

            <li className="nav-item">
              <a className="nav-link active link" aria-current="page" href="/">Home</a>
            </li>

          </ul>
    
          </div>
        </div>
      </nav>


     
      
      <form className="form"  onSubmit={searchNote}>
     

        <input className="form-control-sm form-item" type="search" placeholder="Search the Notes" onChange = {(e) => setSearch(e.target.value)} />

        
        <select name="tag" className="form-control-sm form-select-sm form-item" onChange = {(e) => setSearchTag(e.target.value)}>
          <option value="null">-Apply Filter-</option>
          {tags && tags.tags.map( tag => {
            return(
              <option key={tag} value={tag}>{tag} </option>
            )
          })}
        </select>
 

        <button className="form-item btn btn-outline-info" type="submit"><i className="bi bi-search"></i> Search / <i class="bi bi-filter"></i> Filter</button>


      </form>
    
      
      <div className="row">

        <div className="col-lg-6">         
          <NotesList notes={notes} noteDetail={noteDetail} />
        </div> 

        <div className="col-lg-6">
        {
          page==="detail" && <NoteDetail id={Detail} editNote={editNote} deleteSuccess={Success} />
        }
        {
          page==="editform" && <EditNote note={editedNote} tags={tags} success={Success} />
        }
        {
          page==="addnoteform" && <AddNote tags={tags} success={Success}/>
        }

        {
          page==="addtagform" && <AddTag success={Success}/>
        }
        </div>
      </div>
    </div>
  );
}

export default App;
