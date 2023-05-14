function getDealershipsByState(state) {
  const { CloudantV1 } = require('@ibm-cloud/cloudant');
  const { IamAuthenticator } = require('ibm-cloud-sdk-core');
  const authenticator = new IamAuthenticator({ apikey: '_jmHxOs2-RLKmlfJ2JjQRzEzZ1mnl5bm3SS15Zv66N6d' });
  const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
  });
  cloudant.setServiceUrl('https://39c5ae9d-7f45-4c94-bb02-22a7ce000df0-bluemix.cloudantnosqldb.appdomain.cloud');

  const selector = {
      selector: {
          st: state
      }
  };

  return cloudant.postFind({
      db: 'dealerships',
      ...selector
  })
      .then((result) => {
          let code = 200;
          if (result.result.docs.length === 0) {
              code = 404;
          }
          return {
              statusCode: code,
              headers: { 'Content-Type': 'application/json' },
              body: result.result.docs
          };
      });
}

function main(params) {
  return new Promise(function (resolve, reject) {
      if (params.st) {
          getDealershipsByState(params.st)
              .then((response) => {
                  resolve(response);
              })
              .catch((err) => {
                  reject(err);
              });
      } else {
          const { CloudantV1 } = require('@ibm-cloud/cloudant');
          const { IamAuthenticator } = require('ibm-cloud-sdk-core');
          const authenticator = new IamAuthenticator({ apikey: '_jmHxOs2-RLKmlfJ2JjQRzEzZ1mnl5bm3SS15Zv66N6d' });
          const cloudant = CloudantV1.newInstance({
              authenticator: authenticator
          });
          cloudant.setServiceUrl('https://39c5ae9d-7f45-4c94-bb02-22a7ce000df0-bluemix.cloudantnosqldb.appdomain.cloud');

          cloudant.postAllDocs({ db: 'dealerships', includeDocs: true, limit: 10 })
              .then((result) => {
                  let code = 200;
                  if (result.result.rows.length === 0) {
                      code = 404;
                  }
                  resolve({
                      statusCode: code,
                      headers: { 'Content-Type': 'application/json' },
                      body: result.result.rows
                  });
              })
              .catch((err) => {
                  reject(err);
              });
      }
  });
}
