import pytest


@pytest.fixture
def good_avro():
    return {
        "activityTimestamp": "2021-03-16T12:30:00.904Z",
        "activityType": "USER_GREET",
        "applicationId": "A SERVICE",
        "cdnName": None,
        "description": "We said hello to a user",
        "deviceId": "3255AU249947",
        "generatedId": "alphanum123412id",
        "geoIP": {
            "countryCode": None,
            "ipAddress": "hashedIpAddress123",
        },
        "householdId": "hashedIpAddress12345",
        "ipAddress": "AAAADJVmIzRPWIIpBaU2+QcctCp6LOijcmMLE0bg688E9uSjhTiUTzesVRQw",
        "originatingSystem": "DCM",
        "outcome": "SUCCESS",
        "personaId": "AAAADMtaJFEZFHyGGdvumnd1smXjg4KBIgs9n0ag/0lJ1P70JsaPZc6e4fKE26jh6wNlXZ7YPcEvZR/IaRFGK2zTr3E=",
        "proposition": "MY_SERVICE",
        "provider": "MY_SERVICE",
        "providerTerritory": "GB",
        "assetId": None,
        "serviceKey": None,
        "devicePool": "OUTOFHOME",
        "videoId": "A5EK65Bcwd6MANd5QSkQC",
        "sessionId": None,
        "siteId": None,
        "streamingTicket": "ad2460ba-6a7e-47aa-a729-348ef63289e8",
        "subscriptionType": "TVBOXSETS",
        "syndicatedPlayerHost": None,
        "userId": "hashedUserId123",
        "userType": "CUSTOMER",
        "sdpKafkaOffset": "113031",
        "sdpDIFTimestamp": "2021-03-16T12:30:01Z",
        "sdpSourceTimestamp": None,
        "sdpSourceFileName": None,
        "sdpSubjectId": "hashedUserId123",
        "sdpSourceSystemName": "DCM",
        "sdpSourceEventName": "USER_GREET",
        "sdpSourceTransport": "KAFKA",
        "sdpSourceTerritory": "GB",
        "sdpSourceProvider": "MY_SERVICE",
        "sdpSourceProposition": "MY_SERVICE",
        "sdpSourceOrigin": "DIF",
        "sdpSourceType": "Pub/Sub",
    }


@pytest.fixture
def bad_avro():
    """
    This fixture returns a malformed DIF output with the following invalid properties:
        - sdpSourceProvider != provider
        - sdpSourceProposition != proposition
    """
    return {
        "activityTimestamp": "2021-03-16T12:30:00.904Z",
        "activityType": "USER_GREET",
        "applicationId": "A SERVICE",
        "cdnName": None,
        "description": "We said hello to a user",
        "deviceId": "3255AU249947",
        "generatedId": "alphanum123412id",
        "geoIP": {
            "countryCode": None,
            "ipAddress": "hashedIpAddress123",
        },
        "householdId": "hashedIpAddress12345",
        "ipAddress": "AAAADJVmIzRPWIIpBaU2+QcctCp6LOijcmMLE0bg688E9uSjhTiUTzesVRQw",
        "originatingSystem": "DCM",
        "outcome": "SUCCESS",
        "personaId": "AAAADMtaJFEZFHyGGdvumnd1smXjg4KBIgs9n0ag/0lJ1P70JsaPZc6e4fKE26jh6wNlXZ7YPcEvZR/IaRFGK2zTr3E=",
        "proposition": "MY_SERVICE",
        "provider": "MY_SERVICE",
        "providerTerritory": "GB",
        "assetId": None,
        "serviceKey": None,
        "devicePool": "OUTOFHOME",
        "videoId": "A5EK65Bcwd6MANd5QSkQC",
        "sessionId": None,
        "siteId": None,
        "streamingTicket": "ad2460ba-6a7e-47aa-a729-348ef63289e8",
        "subscriptionType": "TVBOXSETS",
        "syndicatedPlayerHost": None,
        "userId": "hashedUserId123",
        "userType": "CUSTOMER",
        "sdpKafkaOffset": "113031",
        "sdpDIFTimestamp": "2021-03-16T12:30:01Z",
        "sdpSourceTimestamp": None,
        "sdpSourceFileName": None,
        "sdpSubjectId": "hashedUserId123",
        "sdpSourceSystemName": "DCM",
        "sdpSourceEventName": "USER_GREET",
        "sdpSourceTransport": "KAFKA",
        "sdpSourceTerritory": "GB",
        "sdpSourceProvider": "SERVICE_MISMATCH",
        "sdpSourceProposition": "PROP_MISMATCH",
        "sdpSourceOrigin": "DIF",
        "sdpSourceType": "Pub/Sub",
    }


@pytest.fixture
def single_expr():
    return "data['sdpSourceProvider']==data['provider']"


@pytest.fixture
def config():
    return {
        "common_checks": [
            "data['sdpSourceTransport'] == 'KAFKA'",
            "data['sdpSourceOrigin']=='DIF'",
            "data['sdpSourceType']=='Pub/Sub'",
            "data['sdpSourceSystemName']=='DCM'",
        ],
        "feeds": [
            {
                "us-dcm-remove-device-2021-03-16.avro": [
                    "data['sdpSourceEventName']=='USER_GREET'",
                    "data['sdpSourceTerritory']==data['providerTerritory']",
                    "data['sdpSourceProvider']==data['provider']",
                    "data['sdpSourceProposition']==data['proposition']",
                    "validate_timestamp(data['activityTimestamp'], data['sdpSourceTerritory'])",
                    "validate_timestamp(data['activityTimestamp'], data['sdpDIFTimestamp'])",
                ]
            }
        ],
    }
