#ifndef gpHttp_h
#define gpHttp_h

#include "Arduino.h"
#include <WiFi.h>
#include <HTTPClient.h>
#include "gpDebugger.cpp" /* Contains simple command to print to console to debug easily*/

class gpHttp
{
public:
  String makeGET(String url) //was const char*
  {

    http.begin(url, root_ca);
    int httpCode = http.GET();
    String payload = "";
    if (httpCode > 0)
    {
      payload = http.getString();
      gpDebugger::serialPrintln("Payload is: ");
      gpDebugger::serialPrintln(payload);
    }
    else
    {
      gpDebugger::serialPrintln("ERROR :(");
    }
    http.end();
    return payload;
  }

private:
  const char *root_ca_debug = "-----BEGIN CERTIFICATE-----"
                              "MIIFazCCA1OgAwIBAgIUc5eQPLAyZmrErr1JM9+V4aXTMVEwDQYJKoZIhvcNAQEL\n"
                              "BQAwRTELMAkGA1UEBhMCTkwxEzARBgNVBAgMClNvbWUtU3RhdGUxITAfBgNVBAoM\n"
                              "GEludGVybmV0IFdpZGdpdHMgUHR5IEx0ZDAeFw0xOTExMDMxOTA1MDBaFw0yMDEx\n"
                              "MDIxOTA1MDBaMEUxCzAJBgNVBAYTAk5MMRMwEQYDVQQIDApTb21lLVN0YXRlMSEw\n"
                              "HwYDVQQKDBhJbnRlcm5ldCBXaWRnaXRzIFB0eSBMdGQwggIiMA0GCSqGSIb3DQEB\n"
                              "AQUAA4ICDwAwggIKAoICAQCn5KMJ7MjMm/xeozsbGhGNNWIIKbbmQbTeJku0ulGZ\n"
                              "ZA9hZER0g3rR0wfmOU5yZNGSHMMfonflMSx4W+VzIw/sRcNHuKiM6rprAJNOScCZ\n"
                              "VYcABYTy+M+DIPATluEYqNFs/fan85NrDcdzjZN4JsEgtRlUnVarIvgIofm0peyH\n"
                              "EH/wzfodNLsY7U3yZfaio0a/zgcBIvt5NpQF1MMCOfvFl79I1AtYX89K4qZqqRk+\n"
                              "FKmLulhOqHYqvNF5+rCBZ+N8SICy+99oqNUWgy9wEgBHJauYLSHZuWXON6MoYXEu\n"
                              "HeI9b8MJHieb5ZC/udrXqcsE0bZQzohloeOS/RcOpCcvrzJ7ZxKQPuhTt4ZbfE5I\n"
                              "nwAdfQ95yCxigVKYWJJLtVtsepzBKnJg6xpdN/r4NYkx+sGtFcCueucfpTfRqhzv\n"
                              "wOxC1lmMgwfbwJ6bQK1LUlEn9VLgWJEg2K9F3HS+3rUDGDKBBXtrqotcRYQxIUMt\n"
                              "Bjh7CDgoIYk5d3cUaYzpHFcErxvO0Z3ERgRniWuKnAzbt9c14uhs8pARWk4WC55Z\n"
                              "UPVuTuKhwXC/1Cc7MdcKzp/YmLey4PZ61nejr8N1ypg8Q348jsIXnqYnIJW2KQzc\n"
                              "sRwjDN2H4++BGXN/asypnjxqDGR7tJ1LharhlYLunuL1DEhN+Wvu0Aq2unVCugAB\n"
                              "8QIDAQABo1MwUTAdBgNVHQ4EFgQUSk6Y1GqWQlXu/fAmFZ5cshTR45gwHwYDVR0j\n"
                              "BBgwFoAUSk6Y1GqWQlXu/fAmFZ5cshTR45gwDwYDVR0TAQH/BAUwAwEB/zANBgkq\n"
                              "hkiG9w0BAQsFAAOCAgEAVuNYX4Evg/bO/r+zb04uTDkEULhXgjkpCIzdvivWEjQf\n"
                              "gkMWn/Fg5hygZaJ2qxEIpqEHcAyNHyOiH6SAH7cbK9Ga2rLGP0FZA1sjzDft2LDh\n"
                              "k4fFFxZtV+2ZvJNGhWwMSPTvBwbQ1wMFRJHzmmZ6DDBeeE7QMhGBRME8RX/T68D9\n"
                              "HIHO+yJOZLeB3yXZaZKa2F6fPvSh/xJxVBo49VYvee9Eo9Nvt1rdVJwlJfu3j3mN\n"
                              "v2Eb0gRaebtLqXXKpUoatvOxTCjXDZj3pnAlwhcLT/DVbihNq8mcEdp0bb9wT7rg\n"
                              "ja/OFZDhOvqmibbCHulsVf5pBPkYZFlwlIA2fqXQSUJ9PIuu7lJ+xrULPmrJsciL\n"
                              "gaA6fZb7R/Xfwe+O+k+quE3xFgb4aX/hcd4fMdtfd+PJ21N0b1vbS9XEMGLd18jz\n"
                              "PNMC04V2xAcgmS83bTcF4x+zQzMCzsR3Cl4lL6raAbouef2/V6VfBoFB+YMuYxVj\n"
                              "5J+kQEmhRBwCzyARjxZyXwef6ANzJmzDrN0FcVpkMUf74ALtrrE+3eF8R9851nbx\n"
                              "w5OdMblz0PUgBn75bpCIMJx4+vPUE2EO0a2i4bhOI715buN3C/WiHIMtYzAs/zXh\n"
                              "3ToJvk3mgre1HJCkbnYDSQqp9L4T0RMUhmLOUGBIZYu7aa/wjzr/h+Fa1BppieQ=\n"
                              "-----END CERTIFICATE-----";
  const char *root_ca_server = "-----BEGIN CERTIFICATE-----\n"
                               "MIIDSjCCAjKgAwIBAgIQRK+wgNajJ7qJMDmGLvhAazANBgkqhkiG9w0BAQUFADA/\n"
                               "MSQwIgYDVQQKExtEaWdpdGFsIFNpZ25hdHVyZSBUcnVzdCBDby4xFzAVBgNVBAMT\n"
                               "DkRTVCBSb290IENBIFgzMB4XDTAwMDkzMDIxMTIxOVoXDTIxMDkzMDE0MDExNVow\n"
                               "PzEkMCIGA1UEChMbRGlnaXRhbCBTaWduYXR1cmUgVHJ1c3QgQ28uMRcwFQYDVQQD\n"
                               "Ew5EU1QgUm9vdCBDQSBYMzCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEB\n"
                               "AN+v6ZdQCINXtMxiZfaQguzH0yxrMMpb7NnDfcdAwRgUi+DoM3ZJKuM/IUmTrE4O\n"
                               "rz5Iy2Xu/NMhD2XSKtkyj4zl93ewEnu1lcCJo6m67XMuegwGMoOifooUMM0RoOEq\n"
                               "OLl5CjH9UL2AZd+3UWODyOKIYepLYYHsUmu5ouJLGiifSKOeDNoJjj4XLh7dIN9b\n"
                               "xiqKqy69cK3FCxolkHRyxXtqqzTWMIn/5WgTe1QLyNau7Fqckh49ZLOMxt+/yUFw\n"
                               "7BZy1SbsOFU5Q9D8/RhcQPGX69Wam40dutolucbY38EVAjqr2m7xPi71XAicPNaD\n"
                               "aeQQmxkqtilX4+U9m5/wAl0CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNV\n"
                               "HQ8BAf8EBAMCAQYwHQYDVR0OBBYEFMSnsaR7LHH62+FLkHX/xBVghYkQMA0GCSqG\n"
                               "SIb3DQEBBQUAA4IBAQCjGiybFwBcqR7uKGY3Or+Dxz9LwwmglSBd49lZRNI+DT69\n"
                               "ikugdB/OEIKcdBodfpga3csTS7MgROSR6cz8faXbauX+5v3gTt23ADq1cEmv8uXr\n"
                               "AvHRAosZy5Q6XkjEGB5YGV8eAlrwDPGxrancWYaLbumR9YbK+rlmM6pZW87ipxZz\n"
                               "R8srzJmwN0jP41ZL9c8PDHIyh8bwRLtTcm1D9SZImlJnt1ir/md2cXjbDaJWFBM5\n"
                               "JDGFoqgCWjBH4d1QB7wCCZAA62RjYJsWvIjJEubSfZGL+T0yjWW06XyxV3bqxbYo\n"
                               "Ob8VZRzI9neWagqNdwvYkQsEjgfbKbYK7p2CNTUQ\n"
                               "-----END CERTIFICATE-----";
  const char *root_ca = root_ca_server;

  HTTPClient http;
  
};
#endif
