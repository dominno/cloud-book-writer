
import React from 'react';
import { NextPage } from 'next';
import Link from 'next/link';
import { Button } from '@nextui-org/react';

const HomePage: NextPage = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <div className="flex flex-col items-center justify-center">
        <h1 className="text-6xl font-bold">
          Welcome to Cloud Book Writer Platform
        </h1>

        <p className="mt-3 text-2xl">
          Start writing and collaborating on books in the cloud.
        </p>

        <div className="flex mt-6">
          <Link href="/login">
          
              <Button size="lg" type="button" color="secondary">
                Login
              </Button>
          
          </Link>
          <Link href="/register">
            
              <Button size="lg" type="button" color="success" className="ml-4">
                Register
              </Button>
            
          </Link>
        </div>
      </div>
    </div>
  );
};

export default HomePage;

