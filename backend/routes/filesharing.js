const router = require('express').Router()
const auth = require('../auth/auth')





 router.get('/:file_id/getFileDownloaders',auth,async(req,res)=>{
         const file_id =  req.params['file_id']
         // JOIN QUERY
         const query =  `SELECT * FROM sharing where file_id=${file_id}`
         await dbquery(query)
         console.log(query)
         res.status(200).send(query)

 })


router.get('/test',async (req,res)=>{
         const query = `SELECT * FROM user_file where owner_id=1019`
         const user_files = await dbquery(query)
          res.send(user_files)
})

router.post('/updateFileAccessPrivileges/:file_id',auth,async(req,res)=>{
            const file_id = req.params['file_id']
            const user_id =  req.user.id
            const max_download = req.body['max_download']
            const access_code = req.body['access_code']
            const start_datetime = req.body['start_datetime']
            const finish_datetime = req.body['finish_datetime']

            const query = `UPDATE user_file set max_download=${max_download}, access_code='${access_code}' ,
                         start_datetime=${start_datetime} , end_datetime=${finish_datetime} where owner_id=${user_id} and 
                         file_id=${file_id}`

            await dbquery(query)


            res.status(200).send({message: 'All Good'})
})

router.get('/checkFileAccessCode/:code',auth,async(req,res)=>{
                const access_code = req.params['code']

                const query = `SELECT file_id, name, type , size from user_file where access_code='${access_code}'`
                const files = await  dbquery(query)

                if(files.length == 0) {
                      res.status(400).send({message: 'No File matched with this access Code'})
                      return
                }
                res.status(200).send(files[0])

})


router.post('/importFile',auth,async (req,res)=>{
             const user_id = req.user.id
             const access_code = req.body.access_code
             const file_id  = req.body.file_id

            // Checking Access Code
             const query = `SELECT access_code from user_file where file_id='${file_id}'`
             const res1  = await dbquery(query)
             console.log(res1)
             if(res1[0].access_code == access_code) {
                    const query2 = `INSERT INTO sharing values(${file_id},${user_id},0,'${access_code}')`
                    await dbquery(query2)
                 res.status(200).send({message: "Added Successfully"})
             }
             else {

             }
             res.status(500).send({message: 'Internal server Error'})
})















module.exports = router