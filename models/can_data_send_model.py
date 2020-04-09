
class MyBehaviorModel:
    relevant_inputs = []
    relevant_outputs = [
        'TX'
    ]

    def validate(self, inputs, outputs):
        """Returns whether the signals represent correct operation of the device"""
        tx = self.relevant_output_values[0].signal

        print("Data changes: ", list(tx.changes()))

        print("CAN sent?")
            
ModelClass = MyBehaviorModel
