from io import BytesIO
from json import loads
from sys import stderr
from oci.auth import signers
from oci.core import BlockstorageClient
from oci.core.models import UpdateVolumeDetails

def handler(ctx, data: BytesIO = None):
	signer = signers.get_resource_principals_signer()
	bv_client = BlockstorageClient(config={}, signer=signer)
	AlarmEvent = loads(data.getvalue())
	StepValue = AlarmEvent.get("body")
	AlarmData = AlarmEvent.get("alarmMetaData")
	bv_ocid = AlarmData[0]["dimensions"][0]["resourceId"]
	try:
		bv_update_details = UpdateVolumeDetails(vpus_per_gb=int(StepValue))
		bv_update = bv_client.update_volume(bv_ocid, bv_update_details)
		return bv_update.status
	except Exception as E:
		print(E)
