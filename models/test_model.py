
class MyBehaviorModel:
    relevant_inputs = []
    relevant_outputs = [
    	'DataValid',
        'Data0',
        'Data1',
        'Data2',
        'Data3',
    ]

    def validate(self, inputs, outputs):
        """Returns whether the signals represent correct operation of the device"""
        data_valid = self.relevant_output_values[0].signal
        data = [d.signal for d in self.relevant_output_values[1:]]
        change_count = 0
        data_value = 0

        result = []

       	for t, val in data_valid.changes():
       		# rising edge
       		if val == 1: 
       			# Get all four bits as a nibble
       			for i in range(4):
       				data_value = data_value | (data[i].value_at_time(t) << i)

       			if change_count % 2 == 0:
       				data_value = data_value << 4
       			else:
       				result.append(data_value)
       				data_value = 0

       			change_count += 1

       	return bytes(result) == b'BRIANBURKE'

ModelClass = MyBehaviorModel
