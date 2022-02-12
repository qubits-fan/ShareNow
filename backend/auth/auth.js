// For Middle Ware Use
const jwt = require('jsonwebtoken')

const auth = (async (req,res,next)=>{
    try{
           const token = req.header('Authorization').replace('Bearer ','')
           const decrypt = jwt.verify(token,process.env.SECRET_TOKEN)
           const userid = decrypt.id
           if (! userid) {
                return res.status(401).send({
                      message: 'UnAuthorized'
                 })
           }
           const user = await dbquery(`SELECT * FROM auth_user where id=${userid}`)
           console.log(user)
           if(user.length == 0) {
               return res.status(401).send({
                     message: 'UnAuthorized'
               })
           }
           req.user = user[0]
           next()
      }
      catch (e) {

          res.status(500).send({message: e.toString()})
      }
})

module.exports = auth