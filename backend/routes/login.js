const router = require('express').Router()
const { getHashedPassword,getLogInToken,checkPassword } = require('./auth_aux')


router.post('/signup',async(req,res)=>{
          try {
              const email = req.body['email']
              const password = req.body['password']
              const hashedPassword = await  getHashedPassword(password)
              await  dbquery( `INSERT INTO auth_user values (NULL,'${email}','${hashedPassword}')`)
              const ids = await dbquery(`SELECT id FROM auth_user where email='${email}'`)
              const loginToken = await getLogInToken(ids[0].id)
             res.status(200).send({
                  expires: Date.now()+3600*60*1000,
                  token: loginToken
              })
              return

          }
          catch (e) {
              console.log(e)
              res.status(404).send({error: e.toString()})
          }

})


router.post('/login',async(req,res)=>{
             const email = req.body['email']
             const password = req.body['password']

             if(!email || !password) {
                   return res.status(400).send({error: 'Either Email or Password is not Matched'})
             }
             let user = undefined
             try {
                 const query = `SELECT *
                                from auth_user
                                where email = '${email}'`
                 user = await dbquery(query)
             }
             catch (e) {
                 console.log(e)
                  return res.status(500).send({error: 'Sorry Can not Serve this time'})
             }

             if(user.length == 0) {
                 return res.status(400).send({error: 'User not Found'})
             }
             const isMatched = await checkPassword(password,user[0].password)
             if (!isMatched){
                  return res.status(400).send({error: 'Either Password or email id not matched'})
             }

             const loginToken = await getLogInToken(user[0].id)
             res.status(200).send({
                  expires: Date.now()+3600*60*1000,
                  token: loginToken
              })

})









module.exports = router
