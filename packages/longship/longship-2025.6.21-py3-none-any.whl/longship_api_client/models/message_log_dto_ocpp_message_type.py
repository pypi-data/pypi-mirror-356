from enum import Enum


class MessageLogDtoOcppMessageType(str, Enum):
    AUTHORIZE = "Authorize"
    BOOTNOTIFICATION = "BootNotification"
    CANCELRESERVATION = "CancelReservation"
    CHANGEAVAILABILITY = "ChangeAvailability"
    CHANGECONFIGURATION = "ChangeConfiguration"
    CLEARCACHE = "ClearCache"
    CLEARCHARCHINGPROFILE = "ClearCharchingProfile"
    DATATRANSFER = "DataTransfer"
    DIAGNOSTICSSTATUSNOTIFICATION = "DiagnosticsStatusNotification"
    FIRMWARESTATUSNOTIFICATION = "FirmwareStatusNotification"
    GETCOMPOSITESCHEDULE = "GetCompositeSchedule"
    GETCONFIGURATION = "GetConfiguration"
    GETDIAGNOSTICS = "GetDiagnostics"
    GETLOCALLIST = "GetLocalList"
    HEARTBEAT = "Heartbeat"
    METERVALUES = "MeterValues"
    REMOTESTARTTRANSACTION = "RemoteStartTransaction"
    REMOTESTOPTRANSACTION = "RemoteStopTransaction"
    RESERVENOW = "ReserveNow"
    RESET = "Reset"
    SENDLOCALLIST = "SendLocalList"
    SETCHARGINGPROFILE = "SetChargingProfile"
    STARTTRANSACTION = "StartTransaction"
    STATUSNOTIFICATION = "StatusNotification"
    STOPTRANSACTION = "StopTransaction"
    TRANSACTIONEVENT = "TransactionEvent"
    TRIGGERMESSAGE = "TriggerMessage"
    UNLOCKCONNECTOR = "UnlockConnector"
    UPDATEFIRMWARE = "UpdateFirmware"

    def __str__(self) -> str:
        return str(self.value)
