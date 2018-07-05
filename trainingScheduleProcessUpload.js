console.log('Loading function');

const aws = require('aws-sdk');

const s3 = new aws.S3();


/*
Triggered by:  Object Create in 'training-schedule' bucket.
Take incoming file, rename it to training-schedule/ready/current-schedule.csv.
TODO:  At present the copyObject function is not working.  No error, just not working.  Opened issue with support
*/
exports.handler = async (event, context) => {
    console.log('Received event:', JSON.stringify(event, null, 2));

    // Determine the bucket / key of the newly uploaded object:
    var bucket = event.Records[0].s3.bucket.name;
    var key = decodeURIComponent(event.Records[0].s3.object.key.replace(/\+/g, ' '));

    // Copy to /ready folder:
    var params = {
      CopySource: bucket + '/' + key, 
      Bucket: 'training-schedule', 
      Key: 'ready/current-schedule.csv'
     };
    console.log('Source object is: ' + bucket + '/' + key);
    
    s3.copyObject(params, function(err, data) {
    if (err) {
        console.log('An error occurred');
       console.log(err, err.stack); // an error occurred
    } else {
       console.log('copied object ${bucket}/${key} to ${bucket}/ready/current-schedule.csv.');    // successful response
    }
    });        

};
