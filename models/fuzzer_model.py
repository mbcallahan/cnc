
class MyBehaviorModel:
    relevant_inputs = [
        'Serial TX',
    ]
    relevant_outputs = [
        'VALID'
    ]

    def validate(self, inputs, outputs):
        """Returns whether the signals represent correct operation of the device"""
        tx = self.relevant_output_values[0].signal
        rst = self.relevant_output_values[1].signal

        cr = tx.guess_clock_rate()
        if cr == 0:
            return False
        bit_width = 1 / cr

        # Quick single-byte RS232 parser
        byte = 0


        # Use last change in RST as starting point
        t_start, _ = list(rst.changes())[-1]
        i = 0
        for t, _ in tx.changes():
            if t > t_start:
                index_start = i
                break
            i += 1
        else:
            return False

        changes = list(tx.changes())
        if len(changes) < index_start+2:
            return False

        last_t, last_level = changes[index_start]

        found_start = False
        bit_count = 0

        for t, level in changes[index_start+1:]:
            count = round((t - last_t) / bit_width)

            if not found_start and count > 0 and last_level == 0:
                count -= 1
                found_start = True
            
            if found_start and count > 0 and count < 20:
                for i in range(count):
                    byte = byte | (last_level << bit_count)
                    bit_count += 1
            
            if bit_count == 8:
                break

            last_t = t
            last_level = level

        print('Behavior model result:', hex(byte))
        return byte == 0x41
            
ModelClass = MyBehaviorModel
