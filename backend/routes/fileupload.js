const router = require('express').Router()
const auth = require('../auth/auth')
const aws = require('aws-sdk')
const { v4: uuid } = require('uuid')



// AWS Config 1

const s3 = new aws.S3({
    accessKeyId: process.env.AWS_ACCESS_KEY,
    secretAccessKey: process.env.AWS_SECRET_KEY,
    signatureVersion: 'v4'
})


router.post('/fileUpload',auth,async(req,res)=>{
          const userId = req.user.id
          const metadata = req.body
          const name = metadata.name
          const size = metadata.size
          const type = metadata.type
          const file_info = metadata.file_info
          let url = undefined

          const aws_unique_file_key = name + '_' + uuid()
          const fileBuffer = req.files.upload.data
          const fileParams = {
              Bucket: process.env.AWS_BUCKET_NAME,
              Key: aws_unique_file_key,
              Body: fileBuffer
          }

       try{
           const fileRes = await s3.upload(fileParams).promise()
           url = fileRes.Location
           const insertRow = await dbquery(`INSERT INTO user_file values(NULL,'${userId}','${size}','${name}','${type}','${file_info}','${url}',NULL,0,NULL,NULL)`)
       }
       catch(err) {
            res.status(500).send({message: err.toString()})
       }

       res.status(200).send({'message' :  'file Uploaded successfully'})

})

// Shows all Uploaded File and its metadata

router.get('/getYourFiles',auth,async (req,res)=>{
    console.log("got")
    const user = req.user
    const query = `SELECT * FROM user_file where owner_id=${user.id}`
    const user_files = await dbquery(query)
    res.status(200).send(user_files)
})

router.get('/:file_id/:key/download',async (req,res)=>{
            const file_id = req.params['file_id']
            const key = req.params['key']

            const file_param = {
                 Bucket: process.env.AWS_BUCKET_NAME,
                 Key: key,
                 Expires: 600
            }
            s3.getSignedUrl('getObject',file_param,(err,data)=>{
                    if (err){
                          res.status(500).send(err.toString())
                    }
                    const returnData = {
                          signedReq: data
                    }
                           res.status(200).send({message: returnData})
           })
})





























module.exports  = router