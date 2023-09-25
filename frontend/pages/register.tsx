
import React, { useState } from 'react';
import { NextPage } from 'next';
import { useRouter } from 'next/router';
import { Button, Input } from '@nextui-org/react';
import { useForm } from 'react-hook-form';
import { registerUser } from '../utils/api';
import { Controller } from 'react-hook-form';

interface IFormInput {
  username: string;
  password: string;
  email: string;
}

const RegisterPage: NextPage = () => {
  const { register, handleSubmit, formState, control } = useForm<IFormInput>();
  const { errors } = formState;
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const onSubmit = async (data: IFormInput) => {
    setLoading(true);
    try {
      await registerUser(data);
      router.push('/login');
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <h3>Register</h3>
      <form onSubmit={handleSubmit(onSubmit)} className="w-1/3 mt-4">
      <Controller
        name="username"
        control={control} // control is from useForm
        rules={{ required: true }}
        render={({ field }) => (
          <Input
            {...field}
            placeholder="Username"
          />
        )}
      />
      {errors.username && <span>This field is required</span>}
       
      <Controller
        name="password"
        control={control} // control is from useForm
        rules={{ required: true }}
        render={({ field }) => (
          <Input
            {...field}
            type="password"
            placeholder="Password"
            className="mt-4"
          />
        )}
      />
      {errors.password && <span>This field is required</span>}
        <Button
          size="lg"
          type="button"
          className="mt-4"
          isLoading={loading}
        >
          Register
        </Button>
      </form>
    </div>
  );
};

export default RegisterPage;


