import React from "react";


const MapFilter=()=>{
    async function businessFilter(){
        let searchName = document.getElementById('inputAddress').value
        let addrData = {'address': searchName}
        const getData=async()=>{
            let response=await fetch('http://127.0.0.1:8000/api/cleanse/',{
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                  
                },
                body:JSON.stringify(addrData)
            })
            let data = await response.json()
                if (response.status ==200){
                    console.log(data)
    
                }
        }
        getData()
    }
    async function sendBad() {
            const formsData = new FormData();
            const files = document.querySelector("#files2");
            formsData.append("file", files.files[0]);
              let response= await fetch('http://127.0.0.1:8000/api/cleansefile/',{
                  method:'POST',
                  body:formsData,
                  
              })
              let data=await response.json()
              if(response.status===200){
                  console.log(data)
              }
        
     }
    
    return(
        <div className="map-filter">
            <p className="map-stats-title">MAP FILTER</p>
            <div className="search-div">
                <input id='inputAddress' type="text"/>
                <button onClick={businessFilter}> Submit</button>
            </div>

            <div className="fil-upload">
                <input type="file" id="files2" className="test" onClick={sendBad}
        
      style={{display:'none'}}/>
                    <label for="files" className="files-label" style={{marginTop:"5%"}}>
                    Upload
                </label>
            </div>
           
        </div>
    )

}
export default MapFilter;

