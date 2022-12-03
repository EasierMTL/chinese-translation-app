const TextDisplayFooter = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="flex flex-row w-full justify-end p-3 rounded-b-md border-black border-r-2 border-l-2 border-b-2">
      {children}
    </div>
  );
};

export default TextDisplayFooter;
