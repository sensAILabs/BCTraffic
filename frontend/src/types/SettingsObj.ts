enum SenderType {
  pc = "pc",
  mobile = "mobile",
}

export interface SettingsObj {
  experiment_name: string;
  creator_name: string;
  sampling_rate: number;
  comment: number;
  sender_type: SenderType;
}
