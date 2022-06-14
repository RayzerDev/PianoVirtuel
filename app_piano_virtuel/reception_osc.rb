live_loop :foo do
  use_real_time
  note = sync "/osc*/note"
  play note
end