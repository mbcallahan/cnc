
class MyBehaviorModel:
    relevant_inputs = []
    relevant_outputs = [
        'RST',
        'Button',
        'TX'
    ]

    def validate(self, inputs, outputs):
        """Returns whether the signals represent correct operation of the device"""

        rst = self.relevant_output_values[0].signal
        button = self.relevant_output_values[1].signal
        tx = self.relevant_output_values[2].signal

        # Use first change in button as starting point
        t_start, _ = list(button.changes())[1]

        print("Button changes: ", list(button.changes()))
        print("Button pressed at: ", t_start)

        changes = list(tx.changes())
        print("TX changes: ", changes)

        last_t, last_level = changes[-1]
        if(last_level == 1 and last_t > t_start):
            print("Behavior Model validates")
            return True
        else:
            print("Behavior Model does not validate")
            return False
            
ModelClass = MyBehaviorModel
