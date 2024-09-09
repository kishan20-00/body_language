const express = require('express')
var router = express.Router()
var multer = require('multer')
var uniqid = require('uniqid')
const fs = require('fs')

router.post('/upload_base64',function(req, res, next){

  try {

    const send_path = uniqid()

    const path = './public/upload/'+send_path+'.jpg'

    const imgdata = req.body.image;

    const base64Data = imgdata.replace(/^data:([A-Za-z-+/]+);base64,/, '');
    
    fs.writeFileSync(path, base64Data,  {encoding: 'base64'});

    return res.send(send_path+'.jpg');


  } catch (e) {
      next(e)
  }
})

var storage = multer.diskStorage({
    destination: function (req, file, cb) {
    cb(null, 'public/upload')
  },
  filename: function (req, file, cb) {
    cb(null, uniqid() + '-' +file.originalname )
  }
})

var upload = multer({ storage: storage }).single('file')

router.post('/',function(req, res) {
     
    upload(req, res, function (err) {
           if (err instanceof multer.MulterError) {
               return res.status(500).json(err)
           } else if (err) {
               return res.status(500).json(err)
           }
      return res.status(200).send(req.file)

    })

})

module.exports = router