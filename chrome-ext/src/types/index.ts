export type User = {
  id: string;
  email: string;
  created_at: string | Date;
};

export type Career = {
  id: string;
  user_id: string;
  title: string;
  company: string;
  company_location: string;
  job_type: string;
  job_location: string;
  company_description: string;
  description: string[];
  start_date: Date;
  end_date: Date | null;
};

export type UserWithCareers = User & {
  careers: Career[];
};
