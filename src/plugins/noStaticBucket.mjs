export const deploy = {
  start({ cloudformation }) {
    delete cloudformation.Resources.StaticBucket;
    delete cloudformation.Resources.StaticBucketParam;
    delete cloudformation.Resources.StaticBucketPolicy;
    delete cloudformation.Resources.StaticFingerprintParam;
    delete cloudformation.Resources.HTTP.Properties.DefinitionBody.paths[
      "/_static/{proxy+}"
    ];
    delete cloudformation.Resources.GetIndexHTTPLambda.Properties.Environment
      .Variables.ARC_STATIC_BUCKET;
    cloudformation.Resources.Role.Properties.Policies =
      cloudformation.Resources.Role.Properties.Policies.filter(
        ({ PolicyName }) => PolicyName !== "ArcStaticBucketPolicy"
      );
    delete cloudformation.Outputs.BucketURL;
    return cloudformation;
  },
};
