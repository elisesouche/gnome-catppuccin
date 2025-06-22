{ stdenv
, python313
}:

stdenv.mkDerivation {
  pname = "gnome-catppuccin";
  version = "v1.0";

  src = ./.;

  buildInputs = [
    (python313.withPackages (ps: with ps; [
      libsass
      diff-match-patch
    ]))
  ];

  buildPhase = ''
    runHook preBuild
    mkdir -p $out/build
    pushd $out/build
    cp -r $src/* .
    chmod +w -R .
    python3 ./build.py
    popd
    runHook postBuild
  '';

  installPhase = ''
    runHook preInstall
    mkdir -p $out/share/themes/
    mv $out/build/_build/theme/ $out/share/themes/gnome-catppuccin
    rm -r $out/build
    runHook postInstall
  '';

}
