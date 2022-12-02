/**
 * Simple underlined anchor link element with customizable css to reduce code duplication.
 */
function UnderlinedLink({
  children,
  href,
  className = "",
}: {
  children: React.ReactNode;
  href: string;
  className?: string;
}) {
  // Appends new className string
  if (!className.startsWith(" ")) {
    className = "underline " + className;
  } else {
    className = "underline" + className;
  }

  return (
    <a href={href} className={className} target="_blank" rel="noreferrer">
      {children}
    </a>
  );
}

export default UnderlinedLink;
