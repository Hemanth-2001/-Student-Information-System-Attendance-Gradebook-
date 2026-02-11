export interface Student {
  id: number;
  user_id: number;
  admission_number: string;
  roll_number?: string;
  date_of_birth: string;
  gender: Gender;
  blood_group?: BloodGroup;
  nationality: string;
  religion?: string;
  category?: string;
  address_line1?: string;
  address_line2?: string;
  city?: string;
  state?: string;
  pincode?: string;
  country: string;
  medical_conditions?: string;
  allergies?: string;
  medications?: string;
  emergency_contacts?: EmergencyContact[];
  class_id?: number;
  section_id?: number;
  admission_date: string;
  previous_school?: string;
  status: string;
  user?: any;
}

export interface StudentListItem {
  id: number;
  user_id: number;
  admission_number: string;
  roll_number?: string;
  first_name: string;
  last_name: string;
  email: string;
  class_name?: string;
  section_name?: string;
  status: string;
}

export enum Gender {
  MALE = 'male',
  FEMALE = 'female',
  OTHER = 'other'
}

export enum BloodGroup {
  A_POSITIVE = 'A+',
  A_NEGATIVE = 'A-',
  B_POSITIVE = 'B+',
  B_NEGATIVE = 'B-',
  AB_POSITIVE = 'AB+',
  AB_NEGATIVE = 'AB-',
  O_POSITIVE = 'O+',
  O_NEGATIVE = 'O-'
}

export interface EmergencyContact {
  name: string;
  relation: string;
  phone: string;
  alternate_phone?: string;
}

export interface StudentCreate {
  // User info
  email: string;
  username: string;
  password: string;
  first_name: string;
  last_name: string;
  phone?: string;
  
  // Student info
  admission_number: string;
  roll_number?: string;
  date_of_birth: string;
  gender: Gender;
  blood_group?: BloodGroup;
  nationality: string;
  religion?: string;
  category?: string;
  address_line1?: string;
  address_line2?: string;
  city?: string;
  state?: string;
  pincode?: string;
  country: string;
  medical_conditions?: string;
  allergies?: string;
  medications?: string;
  emergency_contacts?: EmergencyContact[];
  class_id?: number;
  section_id?: number;
  admission_date: string;
  previous_school?: string;
  status: string;
}
