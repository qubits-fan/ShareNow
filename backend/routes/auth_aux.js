const bcrypt=require('bcryptjs')
const jwt = require('jsonwebtoken')
const dotenv = require('dotenv')


dotenv.config()
const getHashedPassword = async (password)=>{
    const hashed_pass = await  bcrypt.hash(password,8)
    return hashed_pass
}

const getLogInToken = async(id)=>{
      const token = await jwt.sign({ id: id },process.env.SECRET_TOKEN,{expiresIn: 60*60*60})
      return token
}

const checkPassword = async(password,hashedPassword)=>{
           const isMatched = await  bcrypt.compare(password,hashedPassword)
           return isMatched
 }


module.exports = {
      getHashedPassword,
      getLogInToken,
      checkPassword
}


