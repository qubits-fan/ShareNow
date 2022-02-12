const http = require('http')
const express = require('express')
const mysql = require('mysql')
const dotenv = require('dotenv')
const util = require('util')
const app =  express()
const file_upload = require('express-fileupload')
const fs = require('fs')
dotenv.config()



// Database Connection

const db = mysql.createConnection({
      host:       process.env.DB_HOST,
      user:       process.env.DB_USER,
      password:   process.env.DB_PASSWORD,
      database:   process.env.DB_DATABASE
})

db.connect(function (err){
        if(err) throw err;
        console.log('Database Connected...')
})


global.db = db
global.dbquery = util.promisify(db.query).bind(db)

global.print = (val)=>{
      console.log(val)
}

const gettingData = async()=>{
       let users = await dbquery("SELECT * FROM auth_user")
      console.log(users)
}


// Middle Ware


app.use(express.json())
app.use(file_upload())





//  Routing Set Up
const loginRoute = require('./routes/login')
const fileUploadRoute = require('./routes/fileupload')


// app.use('/fileLoad'),async (req,res)=>{
//   // console.log(req.files.form_field_name.data)
//   //   await fs.writeFileSync('nfile.txt',req.files.form_field_name.data)
//     res.send({uploaded: 'correclty'})
// })
app.use(loginRoute)
app.use(fileUploadRoute)




//
const port = process.env.PORT || 5000



app.listen(port,(connect)=>{
      console.log("The sever is listening on " + port)
})


